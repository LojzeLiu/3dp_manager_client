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
                                         "阿里妈妈方圆体 VF Medium"))

        gSizer3.Add(self.state_label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer3.Add(gSizer3, 1, wx.EXPAND, 5)

        gSizer4 = wx.GridSizer(1, 2, 0, 0)

        self.layer_label = wx.StaticText(self, wx.ID_ANY, "层: 0/0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.layer_label.Wrap(-1)
        self.layer_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                                         "阿里妈妈方圆体 VF Medium"))
        gSizer4.Add(self.layer_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.time_label = wx.StaticText(self, wx.ID_ANY, "--h--m", wx.DefaultPosition, wx.DefaultSize, 0)
        self.time_label.Wrap(-1)
        self.time_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                                        "阿里妈妈方圆体 VF Medium"))
        gSizer4.Add(self.time_label, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        bSizer3.Add(gSizer4, 1, wx.EXPAND, 5)

        self.endtime_label = wx.StaticText(self, wx.ID_ANY, _(u"-- --"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.endtime_label.Wrap(-1)
        self.endtime_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM,
                                           False, "阿里妈妈方圆体 VF Medium"))
        bSizer3.Add(self.endtime_label, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.print_file_name = wx.StaticText(self, wx.ID_ANY, _(u"--"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.print_file_name.Wrap(-1)
        self.print_file_name.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                    "阿里妈妈方圆体 VF Medium"))
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

        # 初始化打印监控服务
        printer_conf = data.PrinterConfInfo()
        printer_conf.setup_table()
        pcl = printer_conf.get_all_conf_info()
        self._printer_service = services.BambuPrinterService(pcl)
        self._printer_service.start_session()

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                             "阿里妈妈方圆体 VF Medium"))

        # 设置菜单字体
        menu_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                            "阿里妈妈方圆体 VF Medium")
        self.m_menubar1 = wx.MenuBar(0)
        self.sys_menu = wx.Menu()
        self.m_menuItem1 = wx.MenuItem(self.sys_menu, wx.ID_ANY, _(u"打印机管理"), wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menuItem1.SetFont(menu_font)
        self.m_full_screen = wx.MenuItem(self.sys_menu, wx.ID_ANY, _(u"全屏"), wx.EmptyString, wx.ITEM_NORMAL)
        self.m_full_screen.SetFont(menu_font)
        self.m_quit_full_screen = wx.MenuItem(self.sys_menu, wx.ID_ANY, _(u"取消全屏"), wx.EmptyString, wx.ITEM_NORMAL)
        self.m_quit_full_screen.SetFont(menu_font)
        self.sys_menu.Append(self.m_menuItem1)
        self.sys_menu.Append(self.m_full_screen)
        self.sys_menu.Append(self.m_quit_full_screen)

        self.m_menubar1.Append(self.sys_menu, _(u"设置"))
        self.m_menu2 = wx.Menu()
        self.m_menuItem2 = wx.MenuItem(self.m_menu2, wx.ID_ANY, _(u"开灯"), wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menuItem2.SetFont(menu_font)
        self.m_menuItem3 = wx.MenuItem(self.m_menu2, wx.ID_ANY, _(u"关灯"), wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menuItem3.SetFont(menu_font)
        self.m_menu2.Append(self.m_menuItem2)
        self.m_menu2.Append(self.m_menuItem3)

        self.m_menubar1.Append(self.m_menu2, _(u"操作"))

        self.SetMenuBar(self.m_menubar1)
        self.m_menubar1.SetFont(menu_font)
        self.m_statusBar1 = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)
        self._printer_infos = []
        self.panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

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

        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_MENU, self.open_light, id=self.m_menuItem2.GetId())
        self.Bind(wx.EVT_MENU, self.close_light, id=self.m_menuItem3.GetId())
        self.Bind(wx.EVT_MENU, self.full_screen, id=self.m_full_screen.GetId())
        self.Bind(wx.EVT_MENU, self.quit_full_screen, id=self.m_quit_full_screen.GetId())
        self.Bind(wx.EVT_MENU, self.on_printer_management, id=self.m_menuItem1.GetId())

        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        # 绑定窗口关闭事件
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Initialize cards for each printer
        self.card_panels = {}
        for idx, printer_info in enumerate(services.PrinterStateList):
            self.add_card(idx, printer_info)

    def on_close(self, event):
        utils.logger.debug('home frame closed')
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

    def open_light(self, event):
        self._printer_service.open_all_light()
        event.Skip()

    def close_light(self, event):
        self._printer_service.close_all_light()
        event.Skip()

    def full_screen(self, event):
        self.ShowFullScreen(True, style=wx.FULLSCREEN_NOCAPTION)
        event.Skip()

    def quit_full_screen(self, event):
        self.ShowFullScreen(False)
        event.Skip()

    def on_key_down(self, event):
        """处理键盘按下事件"""
        print('event.GetKeyCode():', event.GetKeyCode())
        if event.GetKeyCode() == wx.WXK_ESCAPE:  # 检查是否按下 ESC 键
            self.ShowFullScreen(False)  # 退出全屏模式
        else:
            event.Skip()  # 处理其他键的事件


    def on_printer_management(self, event):
        """Show the printer management dialog"""
        dialog = PrinterManagementDialog(self)
        dialog.ShowModal()
        dialog.Destroy()
        event.Skip()  # 处理其他键的事件
