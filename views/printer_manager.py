from tkinter import messagebox

import wx
import wx.grid as gridlib

import models
import utils
from data import PrinterConfInfo
from lib.bpm.bambutools import test_mqtt_connection
from views.composes.custom_message_dialog import CustomMessageDialog


class PrinterGrid(wx.grid.Grid):
    def __init__(self, parent):
        super().__init__(parent)

        # 存储右键菜单事件的绑定ID，用于后续解除绑定
        self._menu_event_bindings = []

        self.CreateGrid(0, 5)  # 初始0行，5列
        self.SetColLabelValue(0, "打印机名称")
        self.SetColLabelValue(1, "IP")
        self.SetColLabelValue(2, "访问码")
        self.SetColLabelValue(3, "机器码")
        self.SetColLabelValue(4, "标签")
        self.AutoSizeColumns()
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.on_right_click)

        # Hide row labels (sequence numbers)
        self.SetRowLabelSize(0)

        # Set grid font
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_MEDIUM, False,
                       models.About.font)
        self.SetDefaultCellFont(font)
        self.SetLabelFont(font)

        self.EnableEditing(False)  # 禁止所有单元格编辑
        # Set selection mode to entire rows
        self.SetSelectionMode(wx.grid.Grid.GridSelectRows)

        self.DisableDragRowSize()  # 禁止调整行高
        self.DisableDragColSize()  # 禁止调整列宽

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
            self.SetCellValue(row, 3, printer.serial_number)
            # Column 4 ("标签") left empty for now

        # Set column widths (total = 800px)
        self.SetColSize(0, 200)  # 打印机名称
        self.SetColSize(1, 120)  # IP
        self.SetColSize(2, 150)  # 访问码
        self.SetColSize(3, 155)  # 机器码
        self.SetColSize(4, 125)  # 标签

    def on_right_click(self, event):
        """右键菜单事件处理"""
        print('on_right_click')
        if event.GetRow() >= 0:  # 确保选中有效行
            self.SelectRow(event.GetRow())
            menu = wx.Menu()

            update_item = menu.Append(wx.ID_ANY, "修改")
            delete_item = menu.Append(wx.ID_ANY, "删除")
            disable_item = menu.Append(wx.ID_ANY, "停用")
            menu.AppendSeparator()
            refresh_item = menu.Append(wx.ID_ANY, "更新")

            binding_id = self.Bind(wx.EVT_MENU, lambda e: self.update_printer(event.GetRow()), update_item)
            self._menu_event_bindings.append(binding_id)
            binding_id = self.Bind(wx.EVT_MENU, lambda e: self.delete_printer(event.GetRow()),
                                   delete_item)  # 修改为调用delete_printer
            self._menu_event_bindings.append(binding_id)
            binding_id = self.Bind(wx.EVT_MENU, lambda e: self.disable_printer(event.GetRow()), disable_item)
            self._menu_event_bindings.append(binding_id)
            binding_id = self.Bind(wx.EVT_MENU, lambda e: self.load_printer_data(), refresh_item)  # 添加刷新功能
            self._menu_event_bindings.append(binding_id)

            self.PopupMenu(menu)
            menu.Destroy()

    def update_printer(self, row):
        """更新打印机信息"""
        current_data = {
            "name": self.GetCellValue(row, 0),
            "hostname": self.GetCellValue(row, 1),
            "access_code": self.GetCellValue(row, 2),
            "serial_number": self.GetCellValue(row, 3)  # 假设序列号未在表格中显示
        }

        # 创建自定义对话框
        dialog = wx.Dialog(self.GetParent(), title="修改打印机信息")
        panel = wx.Panel(dialog)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 名称输入框
        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_label = wx.StaticText(panel, label="名称:")
        name_text = wx.TextCtrl(panel, value=current_data["name"])
        name_sizer.Add(name_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        name_sizer.Add(name_text, 1, wx.ALL | wx.EXPAND, 5)

        # IP地址输入框
        host_sizer = wx.BoxSizer(wx.HORIZONTAL)
        host_label = wx.StaticText(panel, label="IP地址:")
        host_text = wx.TextCtrl(panel, value=current_data["hostname"])
        host_sizer.Add(host_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        host_sizer.Add(host_text, 1, wx.ALL | wx.EXPAND, 5)

        # 访问码输入框
        code_sizer = wx.BoxSizer(wx.HORIZONTAL)
        code_label = wx.StaticText(panel, label="访问码:")
        code_text = wx.TextCtrl(panel, value=current_data["access_code"])
        code_sizer.Add(code_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        code_sizer.Add(code_text, 1, wx.ALL | wx.EXPAND, 5)

        # 机器码输入框
        serial_sizer = wx.BoxSizer(wx.HORIZONTAL)
        serial_label = wx.StaticText(panel, label="机器码:")
        serial_text = wx.TextCtrl(panel, value=current_data["serial_number"])
        serial_sizer.Add(serial_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        serial_sizer.Add(serial_text, 1, wx.ALL | wx.EXPAND, 5)

        # 添加所有控件到主sizer
        sizer.Add(name_sizer, 0, wx.EXPAND)
        sizer.Add(host_sizer, 0, wx.EXPAND)
        sizer.Add(code_sizer, 0, wx.EXPAND)
        sizer.Add(serial_sizer, 0, wx.EXPAND)

        # 修改位置：将按钮直接添加到panel而不是使用CreateButtonSizer
        btn_sizer = wx.StdDialogButtonSizer()
        ok_btn = wx.Button(panel, wx.ID_OK)
        cancel_btn = wx.Button(panel, wx.ID_CANCEL)
        btn_sizer.AddButton(ok_btn)
        btn_sizer.AddButton(cancel_btn)
        btn_sizer.Realize()
        sizer.Add(btn_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        panel.SetSizer(sizer)
        dialog.SetSize(300, 300)  # Set width and height to 300px
        dialog.Fit()

        if dialog.ShowModal() == wx.ID_OK:
            # 更新数据库
            printer_conf = PrinterConfInfo()
            conf_info = models.BambuConfInfo(
                name=name_text.GetValue(),
                hostname=host_text.GetValue(),
                access_code=code_text.GetValue(),
                serial_number=serial_text.GetValue()
            )
            confi_id = printer_conf.get_all_conf_id(name=current_data['name'], hostname=current_data['hostname'],
                                                    access_code=current_data['access_code'])
            if confi_id < 0:
                messagebox.showerror("错误", "不存在的打印机信息")
                return
            printer_conf.update_conf_info(confi_id, conf_info)

            # 更新表格
            self.SetCellValue(row, 0, name_text.GetValue())
            self.SetCellValue(row, 1, host_text.GetValue())
            self.SetCellValue(row, 2, code_text.GetValue())
            self.SetCellValue(row, 3, serial_text.GetValue())

        dialog.Destroy()

    def disable_printer(self, row):
        """标记打印机为停用状态"""
        for col in range(5):
            self.SetCellTextColour(row, col, wx.Colour(128, 128, 128))

    def add_printer(self, name, ip, code, seria_code):
        """添加新打印机行"""

        try:
            db_manager = PrinterConfInfo()  # 实例化数据库管理类
            db_manager.add_config_info(name, ip, code, seria_code)  # 调用add_config_info写入数据库
        except Exception as e:
            utils.logger.error(f"添加打印机到数据库失败: {e}")
            messagebox.showerror("错误", "添加打印机到数据库失败。")
            return

        row = self.GetNumberRows()
        self.AppendRows(1)
        self.SetCellValue(row, 0, name)
        self.SetCellValue(row, 1, ip)
        self.SetCellValue(row, 2, code)
        self.SetCellValue(row, 3, seria_code)
        # self.SetCellValue(row, 4, tags)

    def delete_printer(self, row):
        """删除打印机"""
        printer_conf = PrinterConfInfo()
        confi_id = printer_conf.get_all_conf_id(name=self.GetCellValue(row, 0),
                                                hostname=self.GetCellValue(row, 1),
                                                access_code=self.GetCellValue(row, 2))

        # 弹出确认对话框，提示用户是否确认删除
        confirm_dialog = CustomMessageDialog(
            None,
            f"确认删除打印机：{self.GetCellValue(row, 0)}（主机：{self.GetCellValue(row, 1)}）吗？",
            "删除确认"
        )
        confirm_dialog.ShowModal()

        # 根据用户选择执行操作
        if confirm_dialog.result == wx.ID_YES:
            # 从数据库删除
            printer_conf.delete_conf_info(confi_id)
            # 从表格删除
            self.DeleteRows(row)

        # 销毁对话框
        confirm_dialog.Destroy()


class PrinterManagementDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="打印机管理", size=(800, 600))
        self.panel = wx.Panel(self)
        # self.Bind(wx.EVT_CLOSE, self.on_close)  # 绑定关闭事件
        self.Bind(wx.EVT_WINDOW_DESTROY, self.on_close)

        # Set the background color to white
        self.panel.SetBackgroundColour(wx.Colour(247, 247, 247))
        self.SetBackgroundColour(wx.Colour(247, 247, 247))

        # Set the font for buttons and other controls
        font = wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_MEDIUM, False, models.About.font)

        # 顶部操作条
        self.toolbar = wx.Panel(self.panel)
        self.add_btn = wx.Button(self.toolbar, label="添加打印机", size=(120, 30), style=wx.BORDER_NONE)
        self.del_btn = wx.Button(self.toolbar, label="删除打印机", size=(120, 30), style=wx.BORDER_NONE)

        # 设置按钮背景颜色为 (237, 237, 237)
        bg_color = wx.Colour(237, 237, 237)
        for btn in [self.add_btn, self.del_btn]:
            btn.SetBackgroundColour(bg_color)

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
        main_sizer.Add(self.grid, 1, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        self.panel.SetSizer(main_sizer)

        # 绑定事件
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add_printer)
        self.del_btn.Bind(wx.EVT_BUTTON, self.on_delete_printer)
        self.close_btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CLOSE))

    def on_add_printer(self, event):
        """添加打印机按钮事件 - 使用自定义对话框"""
        # 创建自定义对话框
        dialog = wx.Dialog(self, title="添加打印机")
        panel = wx.Panel(dialog)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 名称输入框
        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_label = wx.StaticText(panel, label="名称:")
        name_text = wx.TextCtrl(panel)
        name_sizer.Add(name_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        name_sizer.Add(name_text, 1, wx.ALL | wx.EXPAND, 5)

        # IP地址输入框
        host_sizer = wx.BoxSizer(wx.HORIZONTAL)
        host_label = wx.StaticText(panel, label="IP地址:")
        host_text = wx.TextCtrl(panel)
        host_sizer.Add(host_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        host_sizer.Add(host_text, 1, wx.ALL | wx.EXPAND, 5)

        # 访问码输入框
        code_sizer = wx.BoxSizer(wx.HORIZONTAL)
        code_label = wx.StaticText(panel, label="访问码:")
        code_text = wx.TextCtrl(panel)
        code_sizer.Add(code_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        code_sizer.Add(code_text, 1, wx.ALL | wx.EXPAND, 5)

        serial_sizer = wx.BoxSizer(wx.HORIZONTAL)
        serial_label = wx.StaticText(panel, label="机器码:")
        serial_text = wx.TextCtrl(panel)
        serial_sizer.Add(serial_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        serial_sizer.Add(serial_text, 1, wx.ALL | wx.EXPAND, 5)

        # 添加所有控件到主sizer
        sizer.Add(name_sizer, 0, wx.EXPAND)
        sizer.Add(host_sizer, 0, wx.EXPAND)
        sizer.Add(code_sizer, 0, wx.EXPAND)
        sizer.Add(serial_sizer, 0, wx.EXPAND)

        # 添加按钮
        btn_sizer = wx.StdDialogButtonSizer()
        ok_btn = wx.Button(panel, wx.ID_OK)
        cancel_btn = wx.Button(panel, wx.ID_CANCEL)
        btn_sizer.AddButton(ok_btn)
        btn_sizer.AddButton(cancel_btn)
        btn_sizer.Realize()
        sizer.Add(btn_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        panel.SetSizer(sizer)
        dialog.SetSize(300, 350)  # 稍微增加高度以适应更多字段
        dialog.Fit()

        while True:
            result = dialog.ShowModal()  # 先存储结果再处理
            if result == wx.ID_OK:
                # 获取所有输入值（在销毁前获取）
                name = name_text.GetValue().strip()
                host = host_text.GetValue().strip()
                code = code_text.GetValue().strip()
                seria = serial_text.GetValue().strip()

                # 验证必要字段
                if name and host and code:
                    self.grid.add_printer(name, host, code, seria)
                    break  # 先退出循环再销毁
                else:
                    wx.MessageBox("名称、IP地址和访问码是必填项", "错误", wx.OK | wx.ICON_ERROR)
                    continue
            else:
                break  # 用户取消，直接退出循环

        dialog.Destroy()  # 统一在循环外销毁对话框

    def on_delete_printer(self, event):
        """删除按钮事件"""
        row = self.grid.GetGridCursorRow()
        if row >= 0:
            self.grid.delete_printer(row)

    def on_close(self, event):
        """关闭对话框时的事件处理"""
        self.grid.Destroy()

        if not self:
            return  # 如果已经被销毁，直接返回
        self.Close()  # 这会触发 EVT_CLOSE 事件
        event.Skip()  # 确保事件继续传递

    # def on_destroy(self, event):
    #     """关闭对话框时的事件处理"""
    #     print('on_destroy')
    #     # self.EndModal(wx.ID_CLOSE)  # 先结束模态
    #     # self.Destroy()  # 再销毁对话框
    #     event.Skip()
