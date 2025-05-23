import models
import utils
from lib.bpm.bambuconfig import BambuConfig
from lib.bpm.bambuprinter import BambuPrinter
from .msg_handle import MsgHandle


class BambuPrinterService:
    """
    拓竹3D打印机功能封装
    """

    def __init__(self, bambu_config: models.BambuConfInfo, msg_handle = None):
        self._bambu_config = bambu_config
        self._bambu_session = None
        self._printer_state = models.PrinterInfo(bambu_config.name, bambu_config.serial_number)

        # 初始化消息相关服务
        send_url = utils.env_set.wechat_send_url
        if msg_handle is None:
            self._msg_handle = MsgHandle(send_url)
        else:
            self._msg_handle = msg_handle


    def start_session(self):
        curr_conf = BambuConfig(self._bambu_config.hostname, self._bambu_config.access_code,
                                self._bambu_config.serial_number, printer_name=self._bambu_config.name)
        self._bambu_session = BambuPrinter(curr_conf)
        self._bambu_session.on_update = self.to_update
        self._bambu_session.start_session()

    def restart_session(self, bambu_config):
        self._bambu_config = bambu_config
        self._quit_session()

        self.start_session()

    def close_sessions(self):
        """
        关闭所有监控对话
        """
        self._msg_handle.stop()  # 停止消息工作队列
        self._quit_session()

    # def switch_voice_info(self):
    #     """开关语音通知"""
    #     return self._msg_handle.switch_voice()

    def _quit_session(self):
        if self._bambu_session is None:
            return
        self._bambu_session.quit()  # 停止打印机监控
        self._bambu_session = None

    def set_state_update(self, value):
        # 设置状态改变时，界面改变回调函数
        self._printer_state.on_update = value

    def to_update(self, printer: BambuPrinter):
        self._printer_state.update_printer_info(printer)

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
                    utils.logger.error(f'Unknown msg type, Code：{code}; Attr:{attr}; item:{item};')

        if printer.gcode_state == "FAILED" and self._printer_state.last_gcode_state == "RUNNING":
            # 发生错误，上一次是在运行中
            msg = f'{self._printer_state.name} 发生错误，请即时处理！'
            print('printer.hms_data:', printer.hms_data)
            if hms_desc is not None:
                msg = f'{self._printer_state.name}，{hms_desc}，请即时处理！'
        elif printer.gcode_state == "FINISH" and self._printer_state.last_gcode_state == "RUNNING":
            msg = f'{self._printer_state.name} 打印完成，请即时收盘！'
            if hms_desc is not None:
                msg = f'{self._printer_state.name}，{hms_desc}，请即时处理！'
        elif printer.gcode_state == "IDLE" and self._printer_state.last_gcode_state == "RUNNING":
            msg = f'{self._printer_state.name} 设备空闲，请即时安排工作！'
            print('printer.hms_data:', printer.hms_data)
            if hms_desc is not None:
                msg = f'{self._printer_state.name}，{hms_desc}，请即时处理！'
        elif printer.gcode_state == "PAUSE" and self._printer_state.last_gcode_state == "RUNNING":
            print('printer.hms_data:', printer.hms_data)
            msg = f'{self._printer_state.name} 设备暂停，请即时查看处理！'
            if hms_desc is not None:
                msg = f'{self._printer_state.name}，{hms_desc}，请即时处理！'
        if msg != "":
            self._msg_handle.add_message(msg, 1)

    def open_light(self):
        if self._bambu_session:
            self._bambu_session.light_state = True

    def close_light(self):
        if self._bambu_session:
            self._bambu_session.light_state = False

    def get_light_state(self):
        if self._bambu_session is None:
            return False
        return self._bambu_session.light_state

    def to_resume_printing(self):
        """
        开始打印
        """
        self._bambu_session.resume_printing()

    def to_pause_printing(self):
        """
        暂停打印
        """
        self._bambu_session.pause_printing()

    def to_stop_printing(self):
        """
        停止打印
        """
        self._bambu_session.stop_printing()

    def get_printer_info(self):
        return self._printer_state
