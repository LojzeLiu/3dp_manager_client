import wx
import gettext

import models

_ = gettext.gettext


class PrinterDetailDialog(wx.Dialog):
    def __init__(self, parent, printer_conf: models.BambuConfInfo, printer_info: models.PrinterInfo):
        super().__init__(parent, title=f"{printer_conf.name} - 详细信息", size=wx.Size(600, 500))

        # 创建布局
        sizer = wx.BoxSizer(wx.VERTICAL)
        h1_title_size = 22
        h2_title_size = 16
        h3_content_size = 12
        grey_color = wx.Colour(139, 139, 139)  # #8b8b8b
        section_bg = wx.Colour(240, 240, 240)  # 分组背景色

        # 设备名称
        self.printer_name = wx.StaticText(self, label=_(printer_info.name))
        self.printer_name.SetFont(wx.Font(h1_title_size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                                          wx.FONTWEIGHT_BOLD, False, models.About.font))

        # 设备信息分组
        info_box = wx.StaticBox(self, label=_("设备信息"))
        info_sizer = wx.StaticBoxSizer(info_box, wx.VERTICAL)

        info_items = [
            _(f"序列号: {printer_conf.serial_number}"),
            _(f"IP地址: {printer_conf.hostname}"),
            _(f"WiFi强度: {printer_info.get_sign_title()}"),
        ]

        for item in info_items:
            text = wx.StaticText(self, label=item)
            text.SetFont(wx.Font(h3_content_size, wx.FONTFAMILY_DEFAULT,
                                 wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))
            text.SetForegroundColour(grey_color)
            info_sizer.Add(text, 0, wx.ALL, 5)

        # 设备状态分组
        status_box = wx.StaticBox(self, label=_("设备状态"))
        self.status_sizer = wx.StaticBoxSizer(status_box, wx.VERTICAL)

        status_text = wx.StaticText(self, label=_(printer_info.gcode_state))
        status_text.SetFont(wx.Font(h3_content_size, wx.FONTFAMILY_DEFAULT,
                                    wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))
        status_text.SetForegroundColour(wx.Colour(printer_info.gcode_state_color))
        self.status_sizer.Add(status_text, 0, wx.ALL, 5)

        # 外挂料盘分组
        filament_box = wx.StaticBox(self, label=_("外挂料盘"))
        filament_sizer = wx.StaticBoxSizer(filament_box, wx.HORIZONTAL)

        filament_btn = wx.Button(self, label=_("PETG"), size=wx.Size(80, 25))
        filament_sizer.Add(filament_btn, 0, wx.ALL, 5)

        # 温度分组
        temp_box = wx.StaticBox(self, label=_("运行实况"))
        self.temp_sizer = wx.StaticBoxSizer(temp_box, wx.HORIZONTAL)

        temp_items = [
            wx.StaticText(self, label=_(f"喷嘴: {printer_info.tool_temp}°C")),
            wx.StaticText(self, label=_(f"热床: {printer_info.bed_temp}°C/{printer_info.bed_temp_target}°C")),
            wx.StaticText(self, label=_(f"速度: {printer_info.speed_level}")),
            wx.StaticText(self, label=_(f"风扇: {printer_info.fan_speed}%/{printer_info.fan_speed_target}%")),
        ]

        for i, item in enumerate(temp_items):
            item.SetFont(wx.Font(h3_content_size, wx.FONTFAMILY_DEFAULT,
                                 wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))
            self.temp_sizer.Add(item, 0, wx.ALL, 5)
            if i < len(temp_items) - 1:
                self.temp_sizer.Add(wx.StaticText(self, label="｜"), 0, wx.ALL, 5)

        # 主布局添加所有分组
        sizer.Add(self.printer_name, 0, wx.EXPAND | wx.ALL, 15)
        sizer.Add(info_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sizer.Add(self.status_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sizer.Add(filament_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sizer.Add(self.temp_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

        self.SetSizer(sizer)
        self.Layout()

        self.SetSizer(sizer)

    def update_info(self, printer_info: models.PrinterInfo):
        """更新显示的打印机信息"""
        # 更新设备名称
        self.printer_name.SetLabel(_(printer_info.name))

        # 更新设备状态
        for child in self.status_sizer.GetStaticBox().GetChildren():
            if isinstance(child, wx.StaticText):
                child.SetLabel(_(printer_info.gcode_state))
                child.SetForegroundColour(wx.Colour(printer_info.gcode_state_color))
                break

        # 更新温度信息
        temp_children = self.temp_sizer.GetStaticBox().GetChildren()
        temp_children[0].SetLabel(_(f"喷嘴: {printer_info.tool_temp}°C"))
        temp_children[2].SetLabel(_(f"热床: {printer_info.bed_temp}°C/{printer_info.bed_temp_target}°C"))
        temp_children[4].SetLabel(_(f"速度: {printer_info.speed_level}"))

        # 强制刷新布局
        self.Layout()
