import asyncio
import threading
import time

import pyttsx3
import requests
import wx

import utils

engine = pyttsx3.init()


class MsgInfo:
    def __init__(self, msg, level):
        self.msg = msg
        self.level = level


class MsgHandle:
    def __init__(self):
        self.msg_queue = asyncio.Queue()  # 消息队列
        self.send_msg_queue = asyncio.Queue()  # 发送消息队列
        self.loop = asyncio.new_event_loop()  # 获取事件循环
        self.send_loop = asyncio.new_event_loop()  # 获取事件循环

        self.worker_thread = threading.Thread(target=self.run_worker)  # 创建线程以运行消息处理程序
        self.worker_thread.start()  # 启动线程

        self.send_worker_thread = threading.Thread(target=self.run_send_worker)  # 创建线程以运行消息处理程序
        self.send_worker_thread.start()  # 启动线程
        self.playing = False

    async def process_message(self, message):
        # 处理消息的逻辑
        engine.setProperty('volume', 1)

        if message.level == 1:
            # 创建确认对话框
            dlg = wx.MessageDialog(None, message.msg, '提示', wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
            dlg.Show()  # 显示对话框

            # 使用线程来播放声音，以避免阻塞主线程
            self.playing = True

            def play_message():
                sleep_count = 5
                sleep_num = 0
                while self.playing:
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

            # 启动播放线程
            play_thread = threading.Thread(target=play_message)
            play_thread.start()

            # 等待用户的响应
            user_response = dlg.ShowModal()  # 模态对话框，等待用户响应

            # 用户点击了确认按钮
            if user_response == wx.ID_OK:
                self.playing = False
            else:
                self.playing = False

            dlg.Destroy()  # 销毁对话框
            play_thread.join()  # 等待播放线程结束
        else:
            engine.say(message.msg)
            engine.runAndWait()

    async def send_messages_to_wechat(self):
        print('run send_messages_to_wechat')
        while True:
            # 发送已记录的消息到微信
            message = await self.send_msg_queue.get()  # 从消息队列中获取消息，若为空则阻塞
            print('send txt:', message.msg)
            self.send_txt_msg_to_wechat(message.msg)
            self.send_msg_queue.task_done()  # 标记消息处理完成

    async def worker(self):
        while True:
            message = await self.msg_queue.get()  # 从消息队列中获取消息，若为空则阻塞
            await self.process_message(message)  # 处理消息
            self.msg_queue.task_done()  # 标记消息处理完成

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
        print('add msg:', message)
        msg = MsgInfo(message, level)
        self.loop.call_soon_threadsafe(self.msg_queue.put_nowait, msg)  # 使用 call_soon_threadsafe 确保线程安全
        self.send_loop.call_soon_threadsafe(self.send_msg_queue.put_nowait, msg)  # 使用 call_soon_threadsafe 确保线程安全

    @staticmethod
    def send_txt_msg_to_wechat(msg):
        headers = {"Content-Type": "application/json"}
        send_url = utils.env_set.WECHAT_SEND_URL
        send_data = {
            "msgtype": "text",  # 消息类型，此时固定为text
            "text": {
                "content": msg,  # 文本内容，最长不超过2048个字节，必须是utf8编码
            }
        }

        res = requests.post(url=send_url, headers=headers, json=send_data)
        print('res:', res.text)


MsgHandler = MsgHandle()
