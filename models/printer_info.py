from lib.bpm.bambuprinter import BambuPrinter
from datetime import datetime, timedelta


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


class PrinterInfo(object):

    def __init__(self):
        self.serial_number = ""
        self.name = ""  # 打印机名称
        self.last_gcode_state = ""  # 上一次打印机状态
        self.gcode_state = ""  # 打印机状态
        self.gcode_state_color = "#06b025"
        self.layer_state = ""  # 打印层数状态
        self.time_remaining = ""  # 剩余时间
        self.end_time = ""  # 预计结束时间
        self.percent_complete = 0  # 完成进度
        self.gcode_file = "--"  # 打印文件名称
        self.light_state = False  # 灯光状态

        self._on_update = None  # 完成进度

    @property
    def on_update(self):
        return self._on_update

    @on_update.setter
    def on_update(self, value):
        self._on_update = value

    def is_change(self, printer: BambuPrinter):
        """
        判断打印机信息是否改变
        """
        if self.serial_number == printer.config.serial_number:
            # 序列号相同，进行对比
            if self.gcode_state != get_gcode_state_title(printer.gcode_state): return True
            if self.layer_state != f'{printer.current_layer}/{printer.layer_count}': return True
            if self.gcode_file != printer.gcode_file: return True
            if self.time_remaining != convert_minutes(printer.time_remaining): return True
            if self.end_time != calculate_future_time(printer.time_remaining): return True
            if self.percent_complete != printer.percent_complete: return True
            if self.light_state != printer.light_state: return True
        return False

    def update_printer_info(self, printer: BambuPrinter):
        """
        更新打印机状态信息
        """
        if self.is_change(printer):
            self.gcode_state = get_gcode_state_title(printer.gcode_state)
            self.gcode_state_color = get_gcode_state_color(printer.gcode_state)
            self.layer_state = f'{printer.current_layer}/{printer.layer_count}'
            self.gcode_file = printer.gcode_file
            self.time_remaining = convert_minutes(printer.time_remaining)
            self.end_time = calculate_future_time(printer.time_remaining)
            self.percent_complete = printer.percent_complete
            self.light_state = printer.light_state
            if self.on_update is not None:
                self.on_update(self)
        self.last_gcode_state = printer.gcode_state


class BambuConfInfo:
    def __init__(self, name, hostname, access_code, serial_number):
        self.name = name
        self.hostname = hostname
        self.access_code = access_code
        self.serial_number = serial_number
