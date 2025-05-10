import wx
import gettext

import models

_ = gettext.gettext


class PrinterDetailDialog(wx.Dialog):
    def __init__(self, parent, printer_conf, printer_info: models.PrinterInfo):
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
            _(f"打印机: {printer_info.serial_number}"),
            _(f"序列号: {printer_info.serial_number}"),
            _(f"设备版本: {printer_info.serial_number}"),
            _(f"IP地址: {printer_info.serial_number}")
        ]

        for item in info_items:
            text = wx.StaticText(self, label=item)
            text.SetFont(wx.Font(h3_content_size, wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))
            text.SetForegroundColour(grey_color)
            info_sizer.Add(text, 0, wx.ALL, 5)

        # 设备状态分组
        status_box = wx.StaticBox(self, label=_("设备状态"))
        status_sizer = wx.StaticBoxSizer(status_box, wx.VERTICAL)

        status_text = wx.StaticText(self, label=_("空闲"))
        status_text.SetFont(wx.Font(h3_content_size, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))
        status_sizer.Add(status_text, 0, wx.ALL, 5)

        # 外挂料盘分组
        filament_box = wx.StaticBox(self, label=_("外挂料盘"))
        filament_sizer = wx.StaticBoxSizer(filament_box, wx.HORIZONTAL)

        filament_btn = wx.Button(self, label=_("PETG"), size=wx.Size(80, 25))
        filament_sizer.Add(filament_btn, 0, wx.ALL, 5)

        # 温度分组
        temp_box = wx.StaticBox(self, label=_("温度"))
        temp_sizer = wx.StaticBoxSizer(temp_box, wx.HORIZONTAL)

        temp_items = [
            wx.StaticText(self, label=_("喷嘴: 21°C")),
            wx.StaticText(self, label=_("热床: 20°C"))
        ]

        for i, item in enumerate(temp_items):
            item.SetFont(wx.Font(h3_content_size, wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))
            temp_sizer.Add(item, 0, wx.ALL, 5)
            if i < len(temp_items)-1:
                temp_sizer.Add(wx.StaticText(self, label="｜"), 0, wx.ALL, 5)

        # 主布局添加所有分组
        sizer.Add(self.printer_name, 0, wx.EXPAND | wx.ALL, 15)
        sizer.Add(info_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sizer.Add(status_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sizer.Add(filament_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sizer.Add(temp_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

        self.SetSizer(sizer)
        self.Layout()

        self.SetSizer(sizer)

    def update_info(self, printer: models.PrinterInfo):
        """更新显示的打印机信息"""
        info = f"""
打印机名称: {printer.name}
序列号: {printer.serial_number}
当前状态: {printer.gcode_state}
打印进度: {printer.percent_complete}%
当前层数: {printer.layer_state}
剩余时间: {printer.time_remaining}
预计完成: {printer.end_time}
打印文件: {printer.gcode_file}
灯光状态: {'开启' if printer.light_state else '关闭'}
        """
        self.info_text.SetValue(info.strip())
