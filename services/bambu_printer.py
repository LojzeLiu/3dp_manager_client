from datetime import datetime, timedelta

import models
import utils
from lib.bpm.bambuconfig import BambuConfig
from lib.bpm.bambuprinter import BambuPrinter
from .msg_handle import MsgHandle

PrinterStateList = []


def calculate_future_time(minutes_to_add):
    """
    计算当前时间加上给定分钟数之后的时间。

    :param minutes_to_add: 要增加的分钟数（整数）
    :return: 计算后的时间字符串，格式为 "YYYY-MM-DD HH:MM"
    """
    if minutes_to_add <= 0:
        return ""
    # 获取当前时间
    current_time = datetime.now()

    # 使用 timedelta 增加分钟
    future_time = current_time + timedelta(minutes=minutes_to_add)

    # 返回计算后的时间字符串
    return future_time.strftime("%Y-%m-%d %H:%M")


def convert_minutes(minutes):
    days = minutes // (24 * 60)
    hours = (minutes % (24 * 60)) // 60
    remaining_minutes = minutes % 60
    result = ""
    if days > 0:
        result += f"{days}天"
    if hours > 0:
        result += f"{hours}时"
    if remaining_minutes > 0:
        result += f"{remaining_minutes}分"
    if result == "":
        result = "0分"
    return result


def get_gcode_state_title(gcode_state):
    if gcode_state == "RUNNING":
        return "打印中"
    elif gcode_state == "FAILED":
        return "发生错误"
    elif gcode_state == "PAUSE":
        return "暂停中"
    elif gcode_state == "IDLE":
        return "空闲中"
    elif gcode_state == "FINISH":
        return "已完成"
    else:
        return gcode_state


def get_gcode_state_color(gcode_state):
    if gcode_state == "RUNNING":
        return "#057748"
    elif gcode_state == "FAILED":
        return "#f20c00"
    elif gcode_state == "PAUSE":
        return "#ffa400"
    elif gcode_state == "IDLE":
        return "#ffa400"
    elif gcode_state == "FINISH":
        return "#ffa400"
    else:
        return "#b200b2"


class BambuPrinterService:
    """
    拓竹3D打印机功能封装
    """

    def __init__(self, bambu_config_list: [models.BambuConfInfo]):
        self._bambu_config_list = bambu_config_list
        self._bambu_session_map = {}

        # 初始化消息相关服务
        send_url = utils.env_set.WECHAT_SEND_URL
        self._msg_handle = MsgHandle(send_url)

        # for bambu_config in self._bambu_config_list:
        #     printer_info = models.PrinterInfo()
        #     printer_info.name = bambu_config.name
        #     printer_info.serial_number = bambu_config.serial_number
        #     PrinterStateList.append(printer_info)

    def start_session(self):
        for bambu_config in self._bambu_config_list:
            curr_conf = BambuConfig(bambu_config.hostname, bambu_config.access_code, bambu_config.serial_number,
                                    printer_name=bambu_config.name)
            curr_printer = BambuPrinter(curr_conf)
            curr_printer.on_update = self.to_update
            curr_printer.start_session()
            self._bambu_session_map[bambu_config.name] = curr_printer
            printer_info = models.PrinterInfo()
            printer_info.name = bambu_config.name
            printer_info.serial_number = bambu_config.serial_number
            PrinterStateList.append(printer_info)

    def restart_session(self, bambu_config_list: [models.BambuConfInfo]):
        self._bambu_config_list = bambu_config_list
        PrinterStateList.clear()
        self._quit_all_session()

        self.start_session()

    def close_all_sessions(self):
        """
        关闭所有监控对话
        """
        self._msg_handle.stop()  # 停止消息工作队列
        self._quit_all_session()

    def _quit_all_session(self):
        for key, printer in self._bambu_session_map.items():
            print('to quit:', key, ';')
            printer.quit()  # 停止打印机监控
        print('to clear map')
        self._bambu_session_map.clear()  # 清空会话映射

    def to_update(self, printer: BambuPrinter):
        for printer_state in PrinterStateList:
            if printer_state.serial_number == printer.config.serial_number:
                printer_state.gcode_state = get_gcode_state_title(printer.gcode_state)
                printer_state.gcode_state_color = get_gcode_state_color(printer.gcode_state)
                printer_state.layer_state = f'{printer.current_layer}/{printer.layer_count}'
                printer_state.gcode_file = printer.gcode_file
                printer_state.time_remaining = convert_minutes(printer.time_remaining)
                printer_state.end_time = calculate_future_time(printer.time_remaining)
                printer_state.percent_complete = printer.percent_complete
                if printer_state.on_update is not None:
                    printer_state.on_update(printer_state)

                # 根据状态做出不同处理
                msg = ""
                hms_desc = None
                if printer.hms_data is not None:
                    for item in printer.hms_data:
                        code = item.get('code', 'N/A')
                        attr = item.get('attr', 'N/A')
                        if 'desc' in item:
                            hms_desc = item['desc']
                            utils.logger.debug(f'hms code:{code}; desc:{hms_desc}; attr:{attr}')
                        else:
                            utils.logger.error(f'Unknown msg type, Code：{code}; Attr:{attr}')

                if printer.gcode_state == "FAILED" and printer_state.last_gcode_state == "RUNNING":
                    # 发生错误，上一次是在运行中
                    msg = f'{printer_state.name} 发生错误，请即时处理！'
                    print('printer.hms_data:', printer.hms_data)
                    if hms_desc is not None:
                        msg = f'{printer_state.name}，{hms_desc}，请即时处理！'
                elif printer.gcode_state == "FINISH" and printer_state.last_gcode_state == "RUNNING":
                    msg = f'{printer_state.name} 打印完成，请即时收盘！'
                    if hms_desc is not None:
                        msg = f'{printer_state.name}，{hms_desc}，请即时处理！'
                elif printer.gcode_state == "IDLE" and printer_state.last_gcode_state == "RUNNING":
                    msg = f'{printer_state.name} 设备空闲，请即时安排工作！'
                    print('printer.hms_data:', printer.hms_data)
                    if hms_desc is not None:
                        msg = f'{printer_state.name}，{hms_desc}，请即时处理！'
                elif printer.gcode_state == "PAUSE" and printer_state.last_gcode_state == "RUNNING":
                    print('printer.hms_data:', printer.hms_data)
                    msg = f'{printer_state.name} 设备暂停，请即时查看处理！'
                    if hms_desc is not None:
                        msg = f'{printer_state.name}，{hms_desc}，请即时处理！'
                if msg != "":
                    self._msg_handle.add_message(msg, 1)
                printer_state.last_gcode_state = printer.gcode_state
                break

    def open_all_light(self):
        for bambu_config in self._bambu_config_list:
            curr_printer = self._bambu_session_map[bambu_config.name]
            curr_printer.light_state = True

    def close_all_light(self):
        for bambu_config in self._bambu_config_list:
            curr_printer = self._bambu_session_map[bambu_config.name]
            curr_printer.light_state = False
