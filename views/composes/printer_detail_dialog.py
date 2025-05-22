import wx
import gettext
import base64
import threading
import time
from io import BytesIO
from PIL import Image

import models
from lib.bpm.bambu_video import BambuCamera

_ = gettext.gettext


class PrinterDetailDialog(wx.Dialog):
    def __init__(self, parent, printer_conf, printer_info):
        wx.Dialog.__init__(self, parent, title=_("打印机详情"), size=wx.Size(850, 650),
                          style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        # 创建一个可滚动的窗口作为主容器
        scrolled_window = wx.ScrolledWindow(self)
        scrolled_window.SetScrollRate(10, 10)  # 设置滚动步长

        # 主布局使用 scrolled_window 替代 self
        sizer = wx.BoxSizer(wx.VERTICAL)
        h1_title_size = 22
        h2_title_size = 16
        h3_content_size = 12
        grey_color = wx.Colour(139, 139, 139)
        section_bg = wx.Colour(240, 240, 240)

        # ========== 打印机名称 ==========
        self.printer_name = wx.StaticText(scrolled_window, label=_(printer_info.name))
        self.printer_name.SetFont(wx.Font(h1_title_size, wx.FONTFAMILY_DEFAULT,
                                        wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))

        # ========== 基本信息分组 ==========
        info_box = wx.StaticBox(scrolled_window, label=_("基本信息"))
        info_sizer = wx.StaticBoxSizer(info_box, wx.HORIZONTAL)

        info_text = wx.StaticText(scrolled_window, label=_(
            f"序列号: {printer_conf.serial_number}\n"
            f"IP地址: {printer_conf.hostname}\n"
            f"WiFi强度: {printer_info.get_sign_title()}"
        ))
        info_text.SetFont(wx.Font(h3_content_size, wx.FONTFAMILY_DEFAULT,
                                wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))
        info_text.SetForegroundColour(grey_color)
        info_sizer.Add(info_text, 0, wx.ALL, 5)

        # 设备状态分组
        status_box = wx.StaticBox(scrolled_window, label=_("设备状态"))
        self.status_sizer = wx.StaticBoxSizer(status_box, wx.VERTICAL)

        status_text = wx.StaticText(scrolled_window, label=_(printer_info.gcode_state))
        status_text.SetFont(wx.Font(h3_content_size, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))
        status_text.SetForegroundColour(wx.Colour(printer_info.gcode_state_color))
        self.status_sizer.Add(status_text, 0, wx.ALL, 5)

        # 外挂料盘分组
        filament_box_title = '外挂料盘'
        if printer_info.ams_exists:
            filament_box_title = 'AMS'
        filament_box = wx.StaticBox(scrolled_window, label=_(filament_box_title))
        filament_sizer = wx.StaticBoxSizer(filament_box, wx.VERTICAL)

        # 创建AMS料盘网格布局，每行4个料盘
        ams_grid_sizer = wx.FlexGridSizer(cols=4, hgap=5, vgap=5)

        for spool_info in printer_info.spools:
            if spool_info.id == 254 and len(printer_info.spools) > 1:
                continue
            # 单个料盘的面板
            spool_panel = wx.Panel(scrolled_window, style=wx.BORDER_SIMPLE)
            spool_panel.SetBackgroundColour(wx.Colour(section_bg))
            spool_sizer = wx.BoxSizer(wx.VERTICAL)
            spool_sizer.AddSpacer(5)  # 顶部间距

            # 1. 显示耗材颜色条
            color_panel = wx.Panel(spool_panel, size=wx.Size(40, 70), style=wx.BORDER_SIMPLE)

            # 处理颜色值（可能是颜色代码或颜色名称）
            if not spool_info.type:  # 当type为空时，设置透明色
                color = section_bg  # 透明色
            elif spool_info.color.startswith('#'):
                color = wx.Colour(spool_info.color)
            else:
                color = wx.NamedColour(spool_info.color) if wx.Colour(spool_info.color).IsOk() else section_bg

            color_panel.SetBackgroundColour(color)
            color_panel.SetToolTip(_(f"颜色: {spool_info.color if spool_info.color else '透明'}"))

            # 2. 显示耗材类型
            type_text_value = spool_info.type if spool_info.type else "空"  # 当type为空时显示"空"
            type_text = wx.StaticText(spool_panel, label=type_text_value)
            type_text.SetFont(wx.Font(h3_content_size, wx.FONTFAMILY_DEFAULT,
                                    wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))

            # 3. 显示线轴ID
            id_title = f"A{spool_info.id + 1}"
            if len(printer_info.spools) == 1:
                id_title = '外挂'
            id_text = wx.StaticText(spool_panel, label=id_title)
            id_text.SetFont(wx.Font(h3_content_size, wx.FONTFAMILY_DEFAULT,
                                   wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))

            # 将控件添加到料盘面板
            spool_sizer.Add(color_panel, 0, wx.ALIGN_CENTER | wx.ALL, 5)
            spool_sizer.Add(type_text, 0, wx.ALIGN_CENTER | wx.TOP, 5)
            spool_sizer.Add(id_text, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)

            spool_panel.SetSizer(spool_sizer)
            ams_grid_sizer.Add(spool_panel, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        filament_sizer.Add(ams_grid_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # 温度分组
        temp_box = wx.StaticBox(scrolled_window, label=_("运行实况"))
        self.temp_sizer = wx.StaticBoxSizer(temp_box, wx.HORIZONTAL)

        temp_items = [
            wx.StaticText(scrolled_window, label=_(f"喷嘴: {printer_info.tool_temp}°C")),
            wx.StaticText(scrolled_window, label=_(f"热床: {printer_info.bed_temp}°C/{printer_info.bed_temp_target}°C")),
            wx.StaticText(scrolled_window, label=_(f"速度: {printer_info.speed_level}")),
            wx.StaticText(scrolled_window, label=_(f"风扇: {printer_info.fan_speed}%/{printer_info.fan_speed_target}%")),
        ]

        for i, item in enumerate(temp_items):
            item.SetFont(wx.Font(h3_content_size, wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))
            self.temp_sizer.Add(item, 0, wx.ALL, 5)
            if i < len(temp_items) - 1:
                self.temp_sizer.Add(wx.StaticText(scrolled_window, label="｜"), 0, wx.ALL, 5)

        # ========== 摄像头画面分组 ==========
        camera_box = wx.StaticBox(scrolled_window, label=_("摄像头画面"))
        camera_sizer = wx.StaticBoxSizer(camera_box, wx.VERTICAL)

        # 创建摄像头画面显示区域
        self.camera_panel = wx.Panel(scrolled_window, size=wx.Size(750, 480))
        self.camera_panel.SetBackgroundColour(wx.Colour(0, 0, 0))  # 黑色背景
        camera_sizer.Add(self.camera_panel, 0, wx.ALL | wx.CENTER, 5)

        # 初始化摄像头线程
        self.camera_thread = None
        self.camera_running = False
        self.camera_image = None

        # 如果打印机配置中有摄像头信息，则启动摄像头
        self.start_camera(printer_conf.hostname, printer_conf.access_code)

        # 主布局添加所有分组
        sizer.Add(self.printer_name, 0, wx.EXPAND | wx.ALL, 15)
        sizer.Add(info_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sizer.Add(self.status_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sizer.Add(filament_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sizer.Add(self.temp_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sizer.Add(camera_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

        # 将主布局设置到滚动窗口
        scrolled_window.SetSizer(sizer)

        # 创建一个外层sizer用于放置滚动窗口
        outer_sizer = wx.BoxSizer(wx.VERTICAL)
        outer_sizer.Add(scrolled_window, 1, wx.EXPAND)
        self.SetSizer(outer_sizer)
        self.Layout()

        # 绑定窗口关闭事件，确保摄像头线程被正确关闭
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def start_camera(self, hostname, access_code):
        """启动摄像头线程"""
        if self.camera_running:
            return

        self.camera_running = True
        self.camera_thread = threading.Thread(
            target=self.update_camera_frame,
            args=(hostname, access_code),
            daemon=True
        )
        self.camera_thread.start()

    def stop_camera(self):
        """停止摄像头线程"""
        self.camera_running = False
        if self.camera_thread and self.camera_thread.is_alive():
            self.camera_thread.join()

    def update_camera_frame(self, hostname, access_code):
        """更新摄像头画面的线程函数"""
        camera = BambuCamera(access_code=access_code, hostname=hostname)
        camera.start()

        while self.camera_running:
            try:
                frame = camera.get_frame()
                if frame:
                    # 将base64编码的图像数据转换为wx.Image
                    img_data = base64.b64decode(frame)
                    pil_image = Image.open(BytesIO(img_data))
                    wx_image = wx.Image(pil_image.size[0], pil_image.size[1])
                    wx_image.SetData(pil_image.convert("RGB").tobytes())

                    # 在主线程中更新UI
                    wx.CallAfter(self.update_camera_ui, wx_image)
                time.sleep(0.1)
            except Exception:
                # utils.logger.error(f"摄像头更新错误: {e}")
                time.sleep(1)

        camera.stop()

    def update_camera_ui(self, wx_image):
        """在主线程中更新摄像头画面"""
        if not self.camera_panel or not wx_image.IsOk():
            return

        # 缩放图像以适应显示区域
        panel_size = self.camera_panel.GetSize()
        scaled_image = wx_image.Scale(panel_size[0], panel_size[1], wx.IMAGE_QUALITY_HIGH)

        # 创建位图并绘制
        bitmap = wx.Bitmap(scaled_image)
        dc = wx.ClientDC(self.camera_panel)
        dc.DrawBitmap(bitmap, 0, 0, True)

    def on_close(self, event):
        """窗口关闭事件处理
        直接关闭窗口，资源释放在后台异步处理，避免阻塞用户交互。
        """
        # 停止摄像头线程（异步，不等待线程结束）
        self.camera_running = False
        if self.camera_thread and self.camera_thread.is_alive():
            # 不调用 join()，避免阻塞主线程
            pass

        # 直接销毁窗口
        self.Destroy()

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
