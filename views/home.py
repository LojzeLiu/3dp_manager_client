import wx
import gettext
import data
import models
import services
import utils
from views import composes
from views.printer_manager import PrinterManagementDialog
from views.setting_dialog import SettingsDialog

_ = gettext.gettext


class HomeFrame(wx.Frame):
    def __init__(self, parent, width=980):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=_(models.About.app_name + " v" + models.About.curr_version),
                          pos=wx.DefaultPosition,
                          size=wx.Size(width, 650), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self._home_width = width
        self._card_width = 430
        self._is_full_screen = False
        self._is_led_open = False
        self._printer_conf_list = []

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                             models.About.font))

        self.m_statusBar1 = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)
        self._printer_infos = []
        self.panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # ========== 新增：顶部控制条 ==========
        # 创建控制条面板
        self.control_bar = wx.Panel(self.panel, size=wx.Size(-1, 60))  # 高度80px适合触摸操作
        control_bar_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 按钮尺寸设置（宽度120px，高度70px适合触摸操作）
        btn_size = wx.Size(60, 60)
        top_btn_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                               models.About.font)
        top_btn_back_color = '#ffffff'

        # LED 灯光控制按钮
        self.top_btn_led_switch = wx.Button(self.control_bar, size=btn_size, style=wx.BORDER_NONE)
        self.top_btn_led_switch.SetBitmap(wx.BitmapBundle(wx.Bitmap(utils.icon_mgr.get_icon('led_close'))))
        self.top_btn_led_switch.SetBackgroundColour(wx.Colour(top_btn_back_color))

        # 全屏控制按钮
        self.top_btn_full_screen = wx.Button(self.control_bar, size=btn_size, style=wx.BORDER_NONE)
        self.top_btn_full_screen.SetBitmap(wx.BitmapBundle(wx.Bitmap(utils.icon_mgr.get_icon('fullscreen-fill'))))
        self.top_btn_full_screen.SetBackgroundColour(wx.Colour(top_btn_back_color))

        # 语音通知开关控制按钮
        self.top_btn_voice_info = wx.Button(self.control_bar, size=btn_size, style=wx.BORDER_NONE)
        self.top_btn_voice_info.SetBitmap(wx.BitmapBundle(wx.Bitmap(utils.icon_mgr.get_icon('volume-up-fill'))))
        self.top_btn_voice_info.SetBackgroundColour(wx.Colour(top_btn_back_color))

        # 打印机管理按钮
        self.top_btn_printer_manager = wx.Button(self.control_bar, size=btn_size, style=wx.BORDER_NONE)
        self.top_btn_printer_manager.SetBitmap(wx.BitmapBundle(wx.Bitmap(utils.icon_mgr.get_icon('printer_manager'))))
        self.top_btn_printer_manager.SetBackgroundColour(wx.Colour(top_btn_back_color))

        # 设置按钮
        self.top_btn_setting = wx.Button(self.control_bar, size=btn_size, style=wx.BORDER_NONE)
        self.top_btn_setting.SetBitmap(wx.BitmapBundle(wx.Bitmap(utils.icon_mgr.get_icon('setting'))))
        self.top_btn_setting.SetBackgroundColour(wx.Colour(top_btn_back_color))

        # 将按钮添加到控制条
        control_bar_sizer.Add(self.top_btn_led_switch, 0, wx.ALL, 5)
        control_bar_sizer.Add(self.top_btn_full_screen, 0, wx.ALL, 5)
        control_bar_sizer.Add(self.top_btn_voice_info, 0, wx.ALL, 5)
        control_bar_sizer.Add(self.top_btn_printer_manager, 0, wx.ALL, 5)

        # 添加弹性空间使按钮靠左
        control_bar_sizer.AddStretchSpacer(1)
        self.control_bar.SetSizer(control_bar_sizer)
        control_bar_sizer.Add(self.top_btn_setting, 0, wx.ALL, 5)

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
        self.Bind(wx.EVT_BUTTON, self.on_show_setting_dialog, self.top_btn_setting)

        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        # 绑定窗口关闭事件
        self.Bind(wx.EVT_CLOSE, self.on_close)
        send_url = utils.env_set.wechat_send_url
        self._msg_handle = services.MsgHandle(send_url)

        # 初始化打印监控服务
        self._on_start_printer()

    def _on_start_printer(self):
        printer_conf = data.PrinterConfInfo()
        printer_conf.setup_table()
        self._printer_conf_list = printer_conf.get_all_conf_info()

        self._card_panels: list[composes.CardPanel] = []
        self.init_cards()

    def _on_restart_printer(self):
        printer_conf = data.PrinterConfInfo()
        printer_conf.setup_table()
        self._printer_conf_list = printer_conf.get_all_conf_info()

        # Clear existing cards
        for card in self._card_panels:
            card.Destroy()
        self._card_panels.clear()
        self.cards_sizer.Clear(delete_windows=True)
        self.init_cards()

        # Force layout update
        self.cards_container.Layout()
        self.cards_container.FitInside()
        self.Layout()

    def on_close(self, event):
        for card_panel in self._card_panels:
            card_panel.to_close_session(event)

        # 确保框架关闭
        self.Destroy()

    def init_cards(self):
        """Add a new card for the given printer."""
        for printer_conf in self._printer_conf_list:
            card = composes.CardPanel(self.cards_container, printer_conf, card_width=self._card_width,
                                      msg_handle=self._msg_handle)
            self.cards_sizer.Add(card, 0, wx.ALL | wx.EXPAND, 5)
            self._card_panels.append(card)
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
            for card_panel in self._card_panels:
                card_panel.to_close_light(event)
            self._is_led_open = False
            btn_icon = 'led_close'
        else:
            # 当前关闭状态，执行开启灯光
            for card_panel in self._card_panels:
                card_panel.to_open_light(event)
            self._is_led_open = True
            btn_icon = 'led_open'
        self.top_btn_led_switch.SetBitmap(wx.BitmapBundle(wx.Bitmap(utils.icon_mgr.get_icon(btn_icon))))
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
        self.top_btn_full_screen.SetBitmap(wx.BitmapBundle(wx.Bitmap(utils.icon_mgr.get_icon(btn_icon))))
        event.Skip()  # 处理其他键的事件

    def on_switch_voice_info(self, event):
        """开关语音通知"""
        switch_state = self._msg_handle.switch_voice()
        # for card_panel in self._card_panels:
        #     switch_state = card_panel.to_switch_voice_info(event)

        if switch_state:
            # 执行完后，是开启状态
            btn_icon = 'volume-up-fill'
        else:
            # 执行完后，是关闭状态
            btn_icon = 'volume-mute-fill'
        self.top_btn_voice_info.SetBitmap(wx.BitmapBundle(wx.Bitmap(utils.icon_mgr.get_icon(btn_icon))))
        event.Skip()  # 处理其他键的事件

    def on_show_setting_dialog(self, event):
        """显示设置窗口"""
        settings_dialog = SettingsDialog(self, self._msg_handle)
        settings_dialog.ShowModal()
        event.Skip()
