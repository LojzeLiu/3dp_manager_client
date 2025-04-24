# 自定义对话框
import wx

import models


class CustomMessageDialog(wx.Dialog):
    def __init__(self, parent, message, title,
                 yes_btn_color="#fc3100", no_btn_color="#1db33c",
                 yes_btn_title="是", no_btn_title="否",
                 show_no_btn=True, center=False):
        super().__init__(parent, title=title)
        self.result = None  # 用于存储用户选择结果
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 消息文本 - 设置宋体12px并居中对齐
        msg_text = wx.StaticText(panel, label=message)
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_NORMAL, faceName=models.About.font)
        msg_text.SetFont(font)
        msg_text.SetWindowStyle(wx.ALIGN_CENTER)  # 文本居中对齐
        main_sizer.Add(msg_text, 1, wx.EXPAND | wx.ALL, 10)  # 使用EXPAND填充空间

        # 底部按钮区域
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 创建"是"按钮（无边框）
        btn_width = 180
        btn_height = 50
        yes_btn = wx.Button(panel, label=yes_btn_title, size=wx.Size(btn_width, btn_height),
                            style=wx.BORDER_NONE)
        yes_btn.SetBackgroundColour(wx.Colour(yes_btn_color))
        # 设置按钮文字样式
        btn_font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL, faceName=models.About.font)
        yes_btn.SetFont(btn_font)
        yes_btn.SetForegroundColour(wx.Colour("#FFFFFF"))  # 白色文字
        yes_btn.Bind(wx.EVT_BUTTON, self.on_yes)

        # 根据参数决定是否创建"否"按钮
        if show_no_btn:
            no_btn = wx.Button(panel, label=no_btn_title, size=wx.Size(btn_width, btn_height),
                               style=wx.BORDER_NONE)
            no_btn.SetBackgroundColour(wx.Colour(no_btn_color))
            no_btn.SetFont(btn_font)
            no_btn.SetForegroundColour(wx.Colour("#FFFFFF"))  # 白色文字
            no_btn.Bind(wx.EVT_BUTTON, self.on_no)
            bottom_sizer.Add(yes_btn, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)  # 居中且右边距5px
            bottom_sizer.Add(no_btn, 0, wx.ALIGN_CENTER | wx.LEFT, 5)  # 居中且左边距5px
        else:
            bottom_sizer.Add(yes_btn, 0, wx.ALIGN_CENTER)

        # 将按钮区域添加到主布局
        main_sizer.Add(bottom_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        panel.SetSizer(main_sizer)
        # 设置窗口固定尺寸
        self.SetSize(wx.Size(400, 200))
        # 禁止用户调整窗口大小
        self.SetWindowStyleFlag(wx.DEFAULT_DIALOG_STYLE & ~wx.RESIZE_BORDER)
        if center:
            # 窗口居中显示
            self.Center()

    def on_yes(self, event):
        self.result = wx.ID_YES
        self.Close()

    def on_no(self, event):
        self.result = wx.ID_NO
        self.Close()
