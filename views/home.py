import wx
import gettext
import data
import models
import services
import utils
from views.printer_manager import PrinterManagementDialog

_ = gettext.gettext


class CardPanel(wx.Panel):
    def __init__(self, parent, printer_info: models.PrinterInfo, card_width=440):
        super(CardPanel, self).__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.Size(card_width, -1),
                                        wx.BORDER_SIMPLE | wx.TAB_TRAVERSAL)
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.SetMinSize(wx.Size(card_width, -1))
        self.SetMaxSize(wx.Size(card_width, -1))

        self.printer_name = printer_info.name
        self._printer = printer_info
        bSizer3 = wx.BoxSizer(wx.VERTICAL)
        gSizer3 = wx.GridSizer(1, 2, 0, 0)

        self.name_label = wx.StaticText(self, wx.ID_ANY, _(self.printer_name), wx.DefaultPosition, wx.DefaultSize,
                                        0)
        self.name_label.Wrap(-1)

        self.name_label.SetFont(
            wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "阿里妈妈方圆体 VF"))

        gSizer3.Add(self.name_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.state_label = wx.StaticText(self, wx.ID_ANY, _(u"状态：--"), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.state_label.Wrap(-1)

        self.state_label.SetFont(wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                                         models.About.font))

        gSizer3.Add(self.state_label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer3.Add(gSizer3, 1, wx.EXPAND, 5)

        gSizer4 = wx.GridSizer(1, 2, 0, 0)

        self.layer_label = wx.StaticText(self, wx.ID_ANY, "层: 0/0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.layer_label.Wrap(-1)
        self.layer_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                                         models.About.font))
        gSizer4.Add(self.layer_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.time_label = wx.StaticText(self, wx.ID_ANY, "--h--m", wx.DefaultPosition, wx.DefaultSize, 0)
        self.time_label.Wrap(-1)
        self.time_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                                        models.About.font))
        gSizer4.Add(self.time_label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        bSizer3.Add(gSizer4, 1, wx.EXPAND, 5)

        self.endtime_label = wx.StaticText(self, wx.ID_ANY, _(u"-- --"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.endtime_label.Wrap(-1)
        self.endtime_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM,
                                           False, models.About.font))
        bSizer3.Add(self.endtime_label, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.print_file_name = wx.StaticText(self, wx.ID_ANY, _(u"--"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.print_file_name.Wrap(-1)
        self.print_file_name.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                    models.About.font))
        bSizer3.Add(self.print_file_name, 0, wx.ALL, 5)

        self.progress_bar = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size(400, 3),
                                     wx.GA_HORIZONTAL)
        self.progress_bar.SetValue(0)
        self.progress_bar.SetMaxSize(wx.Size(400, 3))

        bSizer3.Add(self.progress_bar, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer3)
        self.Layout()

    def update(self, printer):
        """Update the card with the latest printer data."""
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


class HomeFrame(wx.Frame):
    def __init__(self, parent, width=980):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=_(models.About.app_name + " v" + models.About.curr_version),
                          pos=wx.DefaultPosition,
                          size=wx.Size(width, 650), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self._home_width = width
        self._card_width = 430
        self._is_full_screen = False
        self._is_led_open = False

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                             models.About.font))

        self.m_statusBar1 = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)
        self._printer_infos = []
        self.panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # ========== 新增：顶部控制条 ==========
        # 创建控制条面板
        self.control_bar = wx.Panel(self.panel, size=(-1, 60))  # 高度80px适合触摸操作
        control_bar_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 按钮尺寸设置（宽度120px，高度70px适合触摸操作）
        btn_size = wx.Size(60, 60)
        top_btn_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                               models.About.font)
        top_btn_back_color = '#ffffff'

        # LED 灯光控制按钮
        self.top_btn_led_switch = wx.Button(self.control_bar, size=btn_size, style=wx.BORDER_NONE)
        self.top_btn_led_switch.SetBitmap(wx.Bitmap(utils.icon_mgr.get_icon('led_close')))
        self.top_btn_led_switch.SetBackgroundColour(top_btn_back_color)

        # 全屏控制按钮
        self.top_btn_full_screen = wx.Button(self.control_bar, size=btn_size, style=wx.BORDER_NONE)
        self.top_btn_full_screen.SetBitmap(wx.Bitmap(utils.icon_mgr.get_icon('fullscreen-fill')))
        self.top_btn_full_screen.SetBackgroundColour(top_btn_back_color)

        # 语音通知开关控制按钮
        self.top_btn_voice_info = wx.Button(self.control_bar, size=btn_size, style=wx.BORDER_NONE)
        self.top_btn_voice_info.SetBitmap(wx.Bitmap(utils.icon_mgr.get_icon('volume-up-fill')))
        self.top_btn_voice_info.SetBackgroundColour(top_btn_back_color)

        # 打印机管理按钮
        self.top_btn_printer_manager = wx.Button(self.control_bar, size=btn_size, style=wx.BORDER_NONE)
        self.top_btn_printer_manager.SetBitmap(wx.Bitmap(utils.icon_mgr.get_icon('printer_manager')))
        self.top_btn_printer_manager.SetBackgroundColour(top_btn_back_color)

        # 将按钮添加到控制条
        control_bar_sizer.Add(self.top_btn_led_switch, 0, wx.ALL, 5)
        control_bar_sizer.Add(self.top_btn_full_screen, 0, wx.ALL, 5)
        control_bar_sizer.Add(self.top_btn_voice_info, 0, wx.ALL, 5)
        control_bar_sizer.Add(self.top_btn_printer_manager, 0, wx.ALL, 5)

        # 添加弹性空间使按钮靠左
        control_bar_sizer.AddStretchSpacer(1)
        self.control_bar.SetSizer(control_bar_sizer)

        # 将控制条添加到主布局
        main_sizer.Add(self.control_bar, 0, wx.EXPAND | wx.ALL, 0)
        # ========== 控制条结束 ==========

        self.cards_container = wx.ScrolledWindow(self.panel, style=wx.VSCROLL)
        self.cards_container.SetScrollRate(5, 5)
        card_cols_count = int(self._home_width / self._card_width)

        self.cards_sizer = wx.FlexGridSizer(cols=card_cols_count, hgap=5, vgap=5)  # FlexGridSizer for 2 columns
        self.cards_container.SetSizer(self.cards_sizer)
        # Cards Container
        main_sizer.Add(self.cards_container, 1, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(main_sizer)
        self.Layout()
        self.Show()

        # 绑定控制条按钮事件
        self.Bind(wx.EVT_BUTTON, self.on_led_switch, self.top_btn_led_switch)
        self.Bind(wx.EVT_BUTTON, self.on_full_screen, self.top_btn_full_screen)
        self.Bind(wx.EVT_BUTTON, self.on_switch_voice_info, self.top_btn_voice_info)
        self.Bind(wx.EVT_BUTTON, self.on_printer_management, self.top_btn_printer_manager)
        # self.Bind(wx.EVT_BUTTON, self.on_help, self.btn_help)

        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        # 绑定窗口关闭事件
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # 初始化打印监控服务
        self._printer_service = None
        self._on_start_printer()

    def _on_start_printer(self):
        if self._printer_service:
            self._printer_service.close_all_sessions()
            self._printer_service = None
        printer_conf = data.PrinterConfInfo()
        printer_conf.setup_table()
        pcl = printer_conf.get_all_conf_info()
        self._printer_service = services.BambuPrinterService(pcl)
        self._printer_service.start_session()

        # Initialize cards for each printer
        self.card_panels = {}
        for idx, printer_info in enumerate(services.PrinterStateList):
            self.add_card(idx, printer_info)

    def _on_restart_printer(self):
        printer_conf = data.PrinterConfInfo()
        printer_conf.setup_table()
        pcl = printer_conf.get_all_conf_info()
        self._printer_service.restart_session(pcl)

        # Clear existing cards
        for card in self.card_panels.values():
            card.Destroy()
        self.card_panels.clear()
        self.cards_sizer.Clear(delete_windows=True)

        # Create new cards for each printer
        for idx, printer_info in enumerate(services.PrinterStateList):
            self.add_card(idx, printer_info)

        # Force layout update
        self.cards_container.Layout()
        self.cards_container.FitInside()
        self.Layout()

    def on_close(self, event):
        self._printer_service.close_all_sessions()

        # 确保框架关闭
        self.Destroy()

    def add_card(self, idx, printer_info):
        """Add a new card for the given printer."""
        card = CardPanel(self.cards_container, printer_info, card_width=self._card_width, )
        printer_info.on_update = card.update
        self.cards_sizer.Add(card, 0, wx.ALL | wx.EXPAND, 5)
        self.card_panels[idx] = card
        self.cards_container.Layout()
        self.cards_container.FitInside()
        # self.SetSizer( self.cards_sizer )
        # self.Layout()

    def on_resize(self, event):
        """Handle window resize event."""
        # Get the current width of the cards_container
        width = self.GetSize().GetWidth()

        # Each card has a fixed width of 300px, adjust the number of columns accordingly
        card_width = 440
        cols = max(1, width // card_width)  # 计算最大列数
        self.cards_sizer.SetCols(cols)  # 更新列数

        self.Layout()  # 重新布局
        self.cards_container.Layout()  # 重新布局滚动区域
        event.Skip()

    def on_key_down(self, event):
        """处理键盘按下事件"""
        if event.GetKeyCode() == wx.WXK_ESCAPE:  # 检查是否按下 ESC 键
            self.ShowFullScreen(False)  # 退出全屏模式
        else:
            event.Skip()  # 处理其他键的事件

    def on_printer_management(self, event):
        """Show the printer management dialog"""
        dialog = PrinterManagementDialog(self)
        dialog.ShowModal()
        dialog.Destroy()
        self._on_restart_printer()
        event.Skip()  # 处理其他键的事件

    def on_led_switch(self, event):
        """改变所有打印机灯光开关状态"""
        if self._is_led_open:
            # 当前开启状态，执行关闭灯光
            self._printer_service.close_all_light()
            self._is_led_open = False
            btn_icon = 'led_close'
        else:
            # 当前关闭状态，执行开启灯光
            self._printer_service.open_all_light()
            self._is_led_open = True
            btn_icon = 'led_open'
        self.top_btn_led_switch.SetBitmap(wx.Bitmap(utils.icon_mgr.get_icon(btn_icon)))
        event.Skip()  # 处理其他键的事件

    def on_full_screen(self, event):
        """改变窗口全屏状态"""
        if self._is_full_screen:
            # 当前在全屏，退出全屏
            self._is_full_screen = False
            btn_icon = 'fullscreen-fill'
        else:
            # 当前非全屏，进入全屏
            self._is_full_screen = True
            btn_icon = 'fullscreen-exit-fill'
        self.ShowFullScreen(self._is_full_screen)
        self.top_btn_full_screen.SetBitmap(wx.Bitmap(utils.icon_mgr.get_icon(btn_icon)))
        event.Skip()  # 处理其他键的事件

    def on_switch_voice_info(self, event):
        """开关语音通知"""
        switch_state = self._printer_service.switch_voice_info()
        if switch_state:
            # 执行完后，是开启状态
            btn_icon = 'volume-up-fill'
        else:
            # 执行完后，是关闭状态
            btn_icon = 'volume-mute-fill'
        self.top_btn_voice_info.SetBitmap(wx.Bitmap(utils.icon_mgr.get_icon(btn_icon)))
        event.Skip()  # 处理其他键的事件
