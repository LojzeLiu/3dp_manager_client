import wx

from utils import env_set


class IconManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._cache = {}
        return cls._instance

    def get_icon(self, name, size=(32, 32)):
        """获取图标"""
        if name not in self._cache:
            path = f"{env_set.base_dir}/assets/icons/{name}.png"
            img = wx.Image(path, wx.BITMAP_TYPE_ANY)
            img = img.Scale(*size, wx.IMAGE_QUALITY_HIGH)
            self._cache[name] = wx.Bitmap(img)
        return self._cache[name]


icon_mgr = IconManager()
