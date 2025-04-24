import gettext
import wx
import models

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