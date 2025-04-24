import asyncio
import threading
import time

import pyttsx3
import requests
import wx

import utils
from views.composes.custom_message_dialog import CustomMessageDialog

engine = pyttsx3.init()


class MsgInfo:
    def __init__(self, msg, level):
        self.msg = msg
        self.level = level


class MsgHandle:
    def __init__(self, wc_send_url: str):
        self._running = True
        self.msg_queue = asyncio.Queue()  # 消息队列
        self.send_msg_queue = asyncio.Queue()  # 发送消息队列
        self.loop = asyncio.new_event_loop()  # 获取事件循环
        self.send_loop = asyncio.new_event_loop()  # 获取事件循环

        self.worker_thread = threading.Thread(target=self.run_worker)  # 创建线程以运行消息处理程序
        self.worker_thread.start()  # 启动线程

        self.send_worker_thread = threading.Thread(target=self.run_send_worker)  # 创建线程以运行消息处理程序
        self.send_worker_thread.start()  # 启动线程
        self._wc_send_url = wc_send_url
        self._open_voice = True

    def switch_voice(self) -> bool:
        """开关语音通知"""
        self._open_voice = not self._open_voice
        return self._open_voice

    async def process_message(self, message):
        # 处理消息的逻辑
        engine.setProperty('volume', 1)

        if message.level == 1:
            # 使用wx.CallAfter将UI操作调度到主线程
            def show_dialog():
                dlg = CustomMessageDialog(
                    None,
                    message.msg,
                    '提示',
                    yes_btn_title='明 白',
                    show_no_btn=False,
                    yes_btn_color="#1db33c",
                    center=True
                )

                if self._open_voice:
                    self.stop_event = threading.Event()  # 用于控制线程退出

                    def play_message():
                        sleep_count = 5
                        sleep_num = 0
                        while not self.stop_event.is_set():  # 使用Event替代布尔标志
                            if sleep_num >= sleep_count:
                                engine.say(message.msg)
                                engine.runAndWait()
                                sleep_num = 0
                                sleep_count += 5
                                if sleep_count >= 60 * 5:
                                    sleep_count = sleep_count
                            else:
                                sleep_num += 1
                            time.sleep(1)
                        print('to end play message.')

                    play_thread = threading.Thread(target=play_message, daemon=True)  # 设置为守护线程
                    play_thread.start()

                    dlg.ShowModal()
                    self.stop_event.set()  # 通知线程退出
                    dlg.Destroy()
                    play_thread.join(timeout=1)  # 设置超时避免无限等待

            wx.CallAfter(show_dialog)  # 确保对话框在主线程中显示
        else:
            if self._open_voice:
                engine.say(message.msg)
                engine.runAndWait()

    async def send_messages_to_wechat(self):
        while self._running:  # 使用初始化的 _running 属性
            try:
                # 发送已记录的消息到微信
                message = await asyncio.wait_for(self.send_msg_queue.get(), timeout=5.0)  # 从消息队列中获取消息，若为空则阻塞
                self.send_txt_msg_to_wechat(message.msg)
                self.send_msg_queue.task_done()  # 标记消息处理完成
            except asyncio.TimeoutError:
                # 在超时后继续循环
                continue
            except Exception as e:
                utils.logger.error(f"Error in sending message to WeChat: {e}")

    async def worker(self):
        while self._running:  # 使用初始化的 _running 属性
            try:
                message = await asyncio.wait_for(self.msg_queue.get(), timeout=5.0)  # 从消息队列中获取消息，若为空则阻塞
                await self.process_message(message)  # 处理消息
                self.msg_queue.task_done()  # 标记消息处理完成
            except asyncio.TimeoutError:
                # 在超时后继续循环
                continue
            except Exception as e:
                utils.logger.error(f"Error in worker processing message: {e}")
        utils.logger.debug('worker exiting')

    def run_worker(self):
        asyncio.set_event_loop(self.loop)  # 在新线程中设置事件循环
        self.loop.run_until_complete(self.worker())  # 启动 worker 协程

    def run_send_worker(self):
        asyncio.set_event_loop(self.send_loop)  # 在新线程中设置事件循环
        self.send_loop.run_until_complete(self.send_messages_to_wechat())  # 启动 worker 协程

    def add_message(self, message, level=0):
        """
        添加消息
        :param message: 消息内容
        :param level: 消息级别，0：只通知依次；1：无限通知，指导反馈；
        :return:
        """
        # 向消息队列添加消息
        msg = MsgInfo(message, level)
        self.loop.call_soon_threadsafe(self.msg_queue.put_nowait, msg)  # 使用 call_soon_threadsafe 确保线程安全
        self.send_loop.call_soon_threadsafe(self.send_msg_queue.put_nowait, msg)  # 使用 call_soon_threadsafe 确保线程安全

    def send_txt_msg_to_wechat(self, msg):
        if not self._wc_send_url:
            utils.logger.debug(f'wc send url is error:{self._wc_send_url};')
            return
        headers = {"Content-Type": "application/json"}
        send_data = {
            "msgtype": "text",  # 消息类型，此时固定为text
            "text": {
                "content": msg,  # 文本内容，最长不超过2048个字节，必须是utf8编码
            }
        }

        res = requests.post(url=self._wc_send_url, headers=headers, json=send_data)
        if res.status_code != 200:
            utils.logger.debug(f'send msg failed, state code:{res.status_code}, text:{res.text}')
        # print('res:', res.text)

    def stop(self):
        utils.logger.debug(f'to stop')
        self._running = False
