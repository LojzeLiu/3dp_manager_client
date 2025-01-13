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
        self.gcode_file = "--"

        self._on_update = None  # 完成进度

    @property
    def on_update(self):
        return self._on_update

    @on_update.setter
    def on_update(self, value):
        self._on_update = value


class BambuConfInfo:
    def __init__(self, name, hostname, access_code, serial_number):
        self.name = name
        self.hostname = hostname
        self.access_code = access_code
        self.serial_number = serial_number
