import wx
import wx.adv

import models


class SettingsDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="软件设置", size=wx.Size(800, 600),
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        # 主布局：左侧菜单 + 右侧内容面板
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # ========== 左侧菜单 ==========
        # 移除菜单面板的边框（原 style=wx.BORDER_SIMPLE）
        self.menu_panel = wx.Panel(self)
        menu_sizer = wx.BoxSizer(wx.VERTICAL)

        # 菜单项按钮
        self.btn_general = wx.Button(self.menu_panel, label="常规设置", size=wx.Size(150, 40))
        self.btn_notification = wx.Button(self.menu_panel, label="通知设置", size=wx.Size(150, 40))
        self.btn_about = wx.Button(self.menu_panel, label="关于", size=wx.Size(150, 40))

        # 设置按钮样式（扁平化设计）
        for btn in [self.btn_general, self.btn_notification, self.btn_about]:
            btn.SetBackgroundColour(wx.Colour(240, 240, 240))
            btn.SetForegroundColour(wx.Colour(70, 70, 70))
            btn.Bind(wx.EVT_BUTTON, self.on_menu_click)

        # 添加到菜单布局
        menu_sizer.Add(self.btn_general, 0, wx.ALL | wx.EXPAND, 5)
        menu_sizer.Add(self.btn_notification, 0, wx.ALL | wx.EXPAND, 5)
        menu_sizer.Add(self.btn_about, 0, wx.ALL | wx.EXPAND, 5)
        menu_sizer.AddStretchSpacer()  # 填充剩余空间

        self.menu_panel.SetSizer(menu_sizer)
        # 在左侧菜单和右侧内容面板之间添加一条垂直分割线
        main_sizer.Add(self.menu_panel, 0, wx.EXPAND | wx.RIGHT, border=1)
        main_sizer.Add(wx.StaticLine(self, style=wx.LI_VERTICAL), 0, wx.EXPAND)

        # ========== 右侧内容面板 ==========
        # 移除内容面板的边框（原 style=wx.BORDER_SIMPLE）
        self.content_panel = wx.Panel(self)
        self.content_sizer = wx.BoxSizer(wx.VERTICAL)
        self.content_panel.SetSizer(self.content_sizer)
        main_sizer.Add(self.content_panel, 1, wx.EXPAND)

        # 初始化默认页面（常规设置）
        self.current_page = None
        self.show_general_settings()

        self.SetSizer(main_sizer)
        self.Centre()

    def on_menu_click(self, event):
        """菜单按钮点击事件处理"""
        btn = event.GetEventObject()
        if btn == self.btn_general:
            self.show_general_settings()
        elif btn == self.btn_notification:
            self.show_notification_settings()
        elif btn == self.btn_about:
            self.show_about_page()

    def clear_content(self):
        """清空当前内容面板"""
        if self.current_page:
            self.current_page.Destroy()
            self.current_page = None

    def show_general_settings(self):
        """显示常规设置页面"""
        self.clear_content()
        self.current_page = wx.Panel(self.content_panel)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加一个提示文本（实际开发时可替换为具体设置项）
        tip_text = wx.StaticText(self.current_page, label="开发中...")
        tip_text.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        sizer.Add(tip_text, 0, wx.ALL, 20)

        self.current_page.SetSizer(sizer)
        self.content_sizer.Add(self.current_page, 1, wx.EXPAND)
        self.Layout()

    def show_notification_settings(self):
        """显示通知设置页面"""
        self.clear_content()
        self.current_page = wx.Panel(self.content_panel)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 企业微信URL设置
        wx_static = wx.StaticText(self.current_page, label="企业微信通知URL:")
        wx_static.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        self.wx_url = wx.TextCtrl(self.current_page, size=wx.Size(400, -1))

        # 使用GridBagSizer实现更精细的布局
        gb_sizer = wx.GridBagSizer(10, 10)
        gb_sizer.Add(wx_static, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        gb_sizer.Add(self.wx_url, pos=(0, 1), span=(1, 2), flag=wx.EXPAND)

        # 添加保存按钮
        save_btn = wx.Button(self.current_page, label="保存设置")
        save_btn.SetBackgroundColour(wx.Colour(76, 175, 80))  # 绿色按钮
        save_btn.SetForegroundColour(wx.WHITE)
        gb_sizer.Add(save_btn, pos=(1, 2), flag=wx.ALIGN_RIGHT)

        sizer.Add(gb_sizer, 0, wx.ALL, 20)
        self.current_page.SetSizer(sizer)
        self.content_sizer.Add(self.current_page, 1, wx.EXPAND)
        self.Layout()

    def show_about_page(self):
        """显示关于页面"""
        self.clear_content()
        self.current_page = wx.Panel(self.content_panel)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 使用一个垂直布局的主容器，使其内容居中
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        content_sizer = wx.BoxSizer(wx.VERTICAL)  # 内容部分的垂直布局

        # APP 名称
        app_name = wx.StaticText(self.current_page, label=models.About.app_name, style=wx.ALIGN_CENTER)
        app_name.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        # 版本信息
        version_info = wx.StaticText(self.current_page, label=f'Version:{models.About.curr_version}', style=wx.ALIGN_CENTER)
        version_info.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # 作者信息
        author_info = wx.StaticText(self.current_page, label=f'Author:{models.About.author}', style=wx.ALIGN_CENTER)
        author_info.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # 微信二维码标题
        qr_title = wx.StaticText(self.current_page, label="微信扫一扫添加作者好友", style=wx.ALIGN_CENTER)
        qr_title.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # 加载图片并直接缩放到 200x200 像素
        qr_image = wx.Image('assets/icons/author_qr.png', wx.BITMAP_TYPE_PNG)
        qr_image = qr_image.Scale(200, 200, wx.IMAGE_QUALITY_HIGH)
        qr_bitmap = wx.StaticBitmap(self.current_page, bitmap=wx.BitmapBundle.FromBitmap(wx.Bitmap(qr_image)))

        # 检查更新按钮
        update_btn = wx.Button(self.current_page, label="检查更新", size=wx.Size(200, 40))
        update_btn.SetBackgroundColour(wx.Colour(33, 150, 243))  # 蓝色按钮
        update_btn.SetForegroundColour(wx.WHITE)
        update_btn.SetWindowStyleFlag(wx.BORDER_NONE)  # 去除边框
        # 设置字体大小为12px
        font = update_btn.GetFont()
        font.SetPointSize(16)
        update_btn.SetFont(font)

        # 使用FlexGridSizer布局，设置所有控件居中
        fg_sizer = wx.FlexGridSizer(cols=1, vgap=10, hgap=20)
        fg_sizer.Add(app_name, 0, wx.ALIGN_CENTER_HORIZONTAL)
        fg_sizer.Add(version_info, 0, wx.ALIGN_CENTER_HORIZONTAL)
        fg_sizer.Add(author_info, 0, wx.ALIGN_CENTER_HORIZONTAL)
        fg_sizer.Add(qr_bitmap, 0, wx.ALIGN_CENTER_HORIZONTAL)
        fg_sizer.Add(qr_title, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # 将FlexGridSizer添加到内容布局，并设置整体居中
        content_sizer.Add(fg_sizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 30)
        content_sizer.Add(update_btn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 20)

        # 将内容布局添加到主布局，并添加边距使其整体居中
        main_sizer.Add(content_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 30)
        self.current_page.SetSizer(main_sizer)
        self.content_sizer.Add(self.current_page, 1, wx.EXPAND)
        self.Layout()