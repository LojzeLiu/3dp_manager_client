import wx
import wx.grid as gridlib

from data import PrinterConfInfo


def _on_paint_button(self, event):
    btn = event.GetEventObject()
    dc = wx.PaintDC(btn)
    dc.SetBackground(wx.Brush(btn.GetBackgroundColour()))
    dc.Clear()

    # 绘制圆角矩形背景
    rect = btn.GetClientRect()
    radius = 5  # 圆角半径
    dc.SetBrush(wx.Brush(btn.GetBackgroundColour()))
    dc.SetPen(wx.Pen(btn.GetBackgroundColour()))
    dc.DrawRoundedRectangle(rect, radius)

    # 绘制文本
    dc.SetFont(btn.GetFont())
    dc.SetTextForeground(btn.GetForegroundColour())
    label = btn.GetLabel()
    text_width, text_height = dc.GetTextExtent(label)
    dc.DrawText(label, (rect.width - text_width) // 2, (rect.height - text_height) // 2)

class PrinterGrid(gridlib.Grid):
    def __init__(self, parent):
        super().__init__(parent)
        self.CreateGrid(0, 5)  # 初始0行，5列
        self.SetColLabelValue(0, "打印机名称")
        self.SetColLabelValue(1, "IP")
        self.SetColLabelValue(2, "访问码")
        self.SetColLabelValue(3, "备注")
        self.SetColLabelValue(4, "标签")
        self.AutoSizeColumns()
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.on_right_click)


        # Set grid font
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                      wx.FONTWEIGHT_MEDIUM, False, "阿里妈妈方圆体 VF Medium")
        self.SetDefaultCellFont(font)
        self.SetLabelFont(font)

        # Load printer data
        self.load_printer_data()

    def load_printer_data(self):
        """Load printer data from database and populate the grid"""
        # Clear existing data
        if self.GetNumberRows() > 0:
            self.DeleteRows(0, self.GetNumberRows())

        # Get data from database
        printer_conf = PrinterConfInfo()
        printers = printer_conf.get_all_conf_info()

        # Add rows for each printer
        for printer in printers:
            self.AppendRows(1)
            row = self.GetNumberRows() - 1

            # Set values for each column
            self.SetCellValue(row, 0, printer.name)
            self.SetCellValue(row, 1, printer.hostname)
            self.SetCellValue(row, 2, printer.access_code)
            # Column 4 ("标签") left empty for now

        self.AutoSizeColumns()

    def on_right_click(self, event):
        """右键菜单事件处理"""
        if event.GetRow() >= 0:  # 确保选中有效行
            self.SelectRow(event.GetRow())
            menu = wx.Menu()

            update_item = menu.Append(wx.ID_ANY, "更新")
            delete_item = menu.Append(wx.ID_ANY, "删除")
            disable_item = menu.Append(wx.ID_ANY, "停用")
            menu.AppendSeparator()
            refresh_item = menu.Append(wx.ID_ANY, "刷新状态")

            self.Bind(wx.EVT_MENU, lambda e: self.update_printer(event.GetRow()), update_item)
            self.Bind(wx.EVT_MENU, lambda e: self.DeleteRows(event.GetRow()), delete_item)
            self.Bind(wx.EVT_MENU, lambda e: self.disable_printer(event.GetRow()), disable_item)

            self.PopupMenu(menu)
            menu.Destroy()

    def update_printer(self, row):
        """更新打印机信息"""
        current_data = [self.GetCellValue(row, col) for col in range(5)]
        dialog = wx.TextEntryDialog(
            self.GetParent(),
            "修改打印机信息",
            "更新打印机",
            ",".join(current_data)
        )
        if dialog.ShowModal() == wx.ID_OK:
            new_data = dialog.GetValue().split(",")
            if len(new_data) == 5:
                for col, value in enumerate(new_data):
                    self.SetCellValue(row, col, value)
        dialog.Destroy()

    def disable_printer(self, row):
        """标记打印机为停用状态"""
        for col in range(5):
            self.SetCellTextColour(row, col, wx.Colour(128, 128, 128))

    def add_printer(self, name, ip, code, note, tags):
        """添加新打印机行"""
        row = self.GetNumberRows()
        self.AppendRows(1)
        self.SetCellValue(row, 0, name)
        self.SetCellValue(row, 1, ip)
        self.SetCellValue(row, 2, code)
        self.SetCellValue(row, 3, note)
        self.SetCellValue(row, 4, tags)


class PrinterManagementDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="打印机管理", size=(800, 600))
        self.panel = wx.Panel(self)

        # Set the background color to white
        self.panel.SetBackgroundColour(wx.Colour(247, 247, 247))
        self.SetBackgroundColour(wx.Colour(247, 247, 247))

        # Set the font for buttons and other controls
        font = wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                      wx.FONTWEIGHT_MEDIUM, False, "阿里妈妈方圆体 VF Medium")

        # 顶部操作条
        self.toolbar = wx.Panel(self.panel)
        self.add_btn = wx.Button(self.toolbar, label="添加打印机", size=(120, 30), style=wx.BORDER_NONE)
        self.del_btn = wx.Button(self.toolbar, label="删除打印机", size=(120, 30), style=wx.BORDER_NONE)

        # 设置按钮背景颜色为 (237, 237, 237)
        bg_color = wx.Colour(237, 237, 237)
        for btn in [self.add_btn, self.del_btn]:
            btn.SetBackgroundColour(bg_color)
            btn.Bind(wx.EVT_PAINT, _on_paint_button)

        # Apply font to buttons
        self.add_btn.SetFont(font)
        self.del_btn.SetFont(font)

        # 使用BoxSizer实现右侧对齐
        toolbar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        toolbar_sizer.AddStretchSpacer()  # 添加弹性空间
        toolbar_sizer.Add(self.add_btn, 0, wx.ALL, 5)
        toolbar_sizer.Add(self.del_btn, 0, wx.ALL, 5)
        self.toolbar.SetSizer(toolbar_sizer)

        self.add_btn.SetForegroundColour(wx.Colour(0, 174, 104))
        self.del_btn.SetForegroundColour(wx.Colour(0, 174, 104))

        # 表格
        self.grid = PrinterGrid(self.panel)

        # 底部按钮
        self.close_btn = wx.Button(self.panel, wx.ID_CLOSE, "关闭")
        self.close_btn.SetFont(font)  # Apply font to close button

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.close_btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.toolbar, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        self.panel.SetSizer(main_sizer)

        # 绑定事件
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add_printer)
        self.del_btn.Bind(wx.EVT_BUTTON, self.on_delete_printer)
        self.close_btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CLOSE))

    def on_add_printer(self, event):
        """添加打印机按钮事件"""
        dialog = wx.TextEntryDialog(
            self,
            "格式：名称,IP,访问码,备注,标签",
            "添加打印机",
            "打印机1,192.168.1.100,123456,,办公室"
        )
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.GetValue().split(",")
            if len(data) == 5:
                self.grid.add_printer(*[x.strip() for x in data])
        dialog.Destroy()

    def on_delete_printer(self, event):
        """删除按钮事件"""
        row = self.grid.GetGridCursorRow()
        if row >= 0:
            self.grid.DeleteRows(row)