import wx
import gettext
import base64
import threading
import time
from io import BytesIO
from PIL import Image
import models
import utils
from lib.bpm.bambu_video import BambuCamera

_ = gettext.gettext


class PrinterDetailDialog(wx.Dialog):
    def __init__(self, parent, printer_conf: models.BambuConfInfo, printer_info: models.PrinterInfo):
        super().__init__(parent, title=f"{printer_conf.name} - 详细信息", size=wx.Size(800, 1000))

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

        # ========== 摄像头画面分组 ==========
        camera_box = wx.StaticBox(self, label=_("摄像头画面"))
        camera_sizer = wx.StaticBoxSizer(camera_box, wx.VERTICAL)

        # 创建摄像头画面显示区域
        self.camera_panel = wx.Panel(self, size=wx.Size(640, 480))
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

        self.SetSizer(sizer)
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
            except Exception as e:
                utils.logger.error(f"摄像头更新错误: {e}")
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
        """窗口关闭事件处理"""
        event.Skip()
        self.stop_camera()

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
