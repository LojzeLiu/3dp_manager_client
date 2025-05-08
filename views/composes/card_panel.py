import gettext
import wx
import models
import services
import utils
from .custom_message_dialog import CustomMessageDialog

_ = gettext.gettext


class CardPanel(wx.Panel):
    def __init__(self, parent, printer_conf: models.BambuConfInfo, card_width=440):
        super(CardPanel, self).__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.Size(card_width, -1),
                                        wx.BORDER_SIMPLE | wx.TAB_TRAVERSAL)
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.SetMinSize(wx.Size(card_width, -1))
        self.SetMaxSize(wx.Size(card_width, -1))

        self.printer_name = printer_conf.name
        self._printer_conf = printer_conf
        self._printer = services.BambuPrinterService(self._printer_conf)
        self._printer.set_state_update(self.update)
        self._printer.start_session()
        self._is_led_open = False

        b_sizer3 = wx.BoxSizer(wx.VERTICAL)
        g_sizer3 = wx.GridSizer(1, 2, 0, 0)

        self.name_label = wx.StaticText(self, wx.ID_ANY, _(self.printer_name), wx.DefaultPosition, wx.DefaultSize,
                                        0)
        self.name_label.Wrap(-1)

        self.name_label.SetFont(
            wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "阿里妈妈方圆体 VF"))

        g_sizer3.Add(self.name_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.state_label = wx.StaticText(self, wx.ID_ANY, _(u"状态：--"), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.state_label.Wrap(-1)

        self.state_label.SetFont(wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                                         models.About.font))

        g_sizer3.Add(self.state_label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        b_sizer3.Add(g_sizer3, 1, wx.EXPAND, 5)

        g_sizer4 = wx.GridSizer(1, 2, 0, 0)

        self.layer_label = wx.StaticText(self, wx.ID_ANY, "层: 0/0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.layer_label.Wrap(-1)
        self.layer_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                                         models.About.font))
        g_sizer4.Add(self.layer_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.time_label = wx.StaticText(self, wx.ID_ANY, "--h--m", wx.DefaultPosition, wx.DefaultSize, 0)
        self.time_label.Wrap(-1)
        self.time_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                                        models.About.font))
        g_sizer4.Add(self.time_label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        b_sizer3.Add(g_sizer4, 1, wx.EXPAND, 5)

        self.endtime_label = wx.StaticText(self, wx.ID_ANY, _(u"-- --"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.endtime_label.Wrap(-1)
        self.endtime_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM,
                                           False, models.About.font))
        b_sizer3.Add(self.endtime_label, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.print_file_name = wx.StaticText(self, wx.ID_ANY, _(u"--"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.print_file_name.Wrap(-1)
        self.print_file_name.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                    models.About.font))
        b_sizer3.Add(self.print_file_name, 0, wx.ALL, 5)

        self.progress_bar = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size(400, 3),
                                     wx.GA_HORIZONTAL)
        self.progress_bar.SetValue(0)
        self.progress_bar.SetMaxSize(wx.Size(400, 3))

        b_sizer3.Add(self.progress_bar, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        # === 新增操作条 ===
        # 创建操作条面板，高度固定为50px，宽度与卡片相同
        self.control_bar = wx.Panel(self, size=wx.Size(card_width, 50))
        self.control_bar.SetBackgroundColour(wx.Colour(255, 255, 255))  # 浅灰色背景

        # 创建LED控制按钮
        btn_size = wx.Size(40, 40)  # 按钮大小
        top_btn_back_color = "#ffffff"  # 按钮背景色

        self.btn_led_switch = wx.Button(self.control_bar, size=btn_size, style=wx.BORDER_NONE)
        # 设置按钮图标（假设utils.icon_mgr已定义）
        self.btn_led_switch.SetBitmap(wx.BitmapBundle(wx.Bitmap(utils.icon_mgr.get_icon('led_close'))))
        self.btn_led_switch.SetBackgroundColour(wx.Colour(top_btn_back_color))

        # 打印作业继续暂停操作按钮
        self._btn_pla_suspend_state = 'pause-line'
        self.btn_pla_suspend = wx.Button(self.control_bar, size=btn_size, style=wx.BORDER_NONE)
        self.btn_pla_suspend.SetBitmap(wx.BitmapBundle(wx.Bitmap(utils.icon_mgr.get_icon(self._btn_pla_suspend_state))))
        self.btn_pla_suspend.SetBackgroundColour(wx.Colour(top_btn_back_color))
        self.btn_pla_suspend.Disable()

        # 打印作业停止按钮
        self.btn_stop = wx.Button(self.control_bar, size=btn_size, style=wx.BORDER_NONE)
        self.btn_stop.SetBitmap(wx.BitmapBundle(wx.Bitmap(utils.icon_mgr.get_icon('stop-fill'))))
        self.btn_stop.SetBackgroundColour(wx.Colour(top_btn_back_color))
        self.btn_stop.Disable()

        # 将按钮添加到操作条
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        control_sizer.Add(self.btn_led_switch, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        control_sizer.Add(self.btn_pla_suspend, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        control_sizer.Add(self.btn_stop, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        self.control_bar.SetSizer(control_sizer)

        # 将操作条添加到主布局
        b_sizer3.Add(self.control_bar, 0, wx.EXPAND | wx.TOP, 5)
        # === 操作条添加结束 ===

        # 绑定按钮事件
        self.Bind(wx.EVT_BUTTON, self.switch_light, self.btn_led_switch)
        self.Bind(wx.EVT_BUTTON, self.on_switch_print, self.btn_pla_suspend)

        self.SetSizer(b_sizer3)
        self.Layout()

    def update(self, printer: models.PrinterInfo):
        """Update the card with the latest printer data."""
        # 根据打印状态，更新打印作业操作按钮
        self.on_update_ope_btn_state(printer.gcode_state)
        self.on_update_light_state(printer.light_state, True)
        is_change = False
        if self.state_label.GetLabel() != printer.gcode_state:
            self.state_label.SetForegroundColour(wx.Colour(printer.gcode_state_color))
            self.state_label.SetLabel(f"{printer.gcode_state}")
            is_change = True

        layer_label = f"层: {printer.layer_state}"
        if self.time_label.GetLabel() != layer_label:
            self.layer_label.SetLabel(layer_label)
            is_change = True
        if self.time_label.GetLabel() != printer.time_remaining:
            self.time_label.SetLabel(printer.time_remaining)
            is_change = True
        if printer.end_time != "" and self.endtime_label.GetLabel() != printer.end_time:
            self.endtime_label.SetLabel(printer.end_time)
            is_change = True
        if self.print_file_name.GetLabel() != printer.gcode_file:
            self.print_file_name.SetLabel(printer.gcode_file)
            is_change = True
        if self.progress_bar.GetValue() != printer.percent_complete:
            self.progress_bar.SetValue(printer.percent_complete)
            is_change = True

        if is_change:
            self.Layout()

    def switch_light(self, event):
        """
        打印机灯光开关
        """
        if self._is_led_open:
            self.to_close_light(event)
        else:
            self.to_open_light(event)

    def to_open_light(self, event):
        """
        打开打印机LED灯光
        """
        self.btn_led_switch.Disable()
        self._printer.open_light()
        self.on_update_light_state(True)
        event.Skip()

    def to_close_light(self, event):
        """
        关闭打印机LED灯光
        """
        self.btn_led_switch.Disable()
        self._printer.close_light()
        self.on_update_light_state(False)
        event.Skip()

    def to_switch_voice_info(self, event):
        """
        改变打印机语音通知状态
        """
        state = self._printer.switch_voice_info()
        event.Skip()
        return state

    def to_close_session(self, event):
        """
        关闭打印机状态监听对话
        """
        self._printer.close_sessions()
        event.Skip()

    def on_update_light_state(self, state, enable_btn=False):
        """
        更新灯光状态
        """
        if enable_btn: self.btn_led_switch.Enable()
        if state == self._is_led_open:
            # 灯光状态相同什么都不做
            return
        self._is_led_open = state
        if self._is_led_open:
            # 灯光开启状态
            btn_icon = 'led_open'
        else:
            btn_icon = 'led_close'
        self.btn_led_switch.SetBitmap(wx.BitmapBundle(wx.Bitmap(utils.icon_mgr.get_icon(btn_icon))))

    def on_update_ope_btn_state(self, gcode_state: str):
        """
        根据打印机状态，调整操作按钮
        """
        if gcode_state == "打印中":
            # 当前机器正在打印中，按钮显示：暂停、停止
            self._btn_pla_suspend_state = 'pause-line'
            self.btn_stop.Enable()
        elif gcode_state == "发生错误" or gcode_state == "暂停中":
            # 当前机器发生错误或者暂停中，按钮显示：开始、停止
            self._btn_pla_suspend_state = 'play-line'
            self.btn_stop.Enable()
        elif gcode_state == "空闲中" or gcode_state == "已完成":
            # 当前机器空闲中或者已完成，按钮显示：开始、停止（禁用）
            self._btn_pla_suspend_state = 'play-line'
            self.btn_stop.Disable()
        else:
            utils.logger.debug(f'{self._printer_conf.name}; unknow gcode state:{gcode_state}；')
        self.btn_pla_suspend.SetBitmap(wx.BitmapBundle(wx.Bitmap(utils.icon_mgr.get_icon(self._btn_pla_suspend_state))))
        self.btn_pla_suspend.Enable()

    def on_switch_print(self, event):
        if self._btn_pla_suspend_state == 'pause-line':
            self._printer.to_pause_printing()
        elif self._btn_pla_suspend_state == 'play-line':
            self._printer.to_resume_printing()
        self.btn_pla_suspend.Disable()
        event.Skip()

    def on_stop_print(self, event):
        """
        停止打印
        """
        confirm_dialog = CustomMessageDialog(
            None,
            f"确定停止本次任务吗？注意该操作无法撤销！",
            "停止确认",
            yes_btn_title="停 止", no_btn_title="取 消"
        )
        confirm_dialog.ShowModal()

        # 根据用户选择执行操作
        if confirm_dialog.result == wx.ID_YES:
            self._printer.to_stop_printing()
            self.btn_stop.Disable()
        event.Skip()
