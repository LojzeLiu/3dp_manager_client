class BambuSpool:
    """
    这个值对象由 `BambuPrinter` 使用，用于枚举连接到打印机的“线轴”。
    它主要用于 `BambuPrinter` 的 `_spools` 属性中，并在机器上有活动的线轴时作为元组的一部分返回。
    """    
    def __repr__(self):
        return str(self)
    def __str__(self):
        return f"id=[{self.id}] tray_info_idx=[{self.tray_info_idx}] name=[{self.name}] type=[{self.type}] sub brands=[{self.sub_brands}] color=[{self.color}] k=[{self.k}] bed_temp=[{self.bed_temp}] nozzle_temp_min=[{self.nozzle_temp_min}] nozzle_temp_max=[{self.nozzle_temp_max}]"
    
    def __init__(self, id: int, name: str, type: str, sub_brands: str, color: str, tray_info_idx : str, k : float, bed_temp : int, nozzle_temp_min : int, nozzle_temp_max : int):
        """
        为 `BambuSpool` 设置所有内部存储属性。

        参数
        ----------
        * id : int - 线轴 ID，可以是 `0-3`（AMS 线轴）或 `254`（外部线轴）。
        * name : str - 线轴的名称，通常仅在 AMS 识别到 Bambu Lab RFID 标签时填充。
        * type : str - 线轴中的耗材类型，可以通过 RFID 标签读取或在打印机显示屏上设置。
        * sub_brands : str - 对于 Bambu Lab 耗材，指定耗材的特殊类型（如 Matte、Pro、Tough 等）。
        * color : str - 可以是颜色十六进制代码，或者如果 `webcolors` 能够识别颜色代码，则为颜色名称。
        * tray_info_idx : str - 在 Bambu Studio 中选定耗材的底层索引。
        * k : float - 用于确定最佳线性推进（流量）的 K 因子。
        * bed_temp : int - 使用的目标热床温度。
        * nozzle_temp_min : int - 可用的最低喷嘴温度。
        * nozzle_temp_max : int - 可用的最高喷嘴温度。
        """
        self.id = id
        self.name = name
        self.type = type
        self.sub_brands = sub_brands
        self.color = color
        self.tray_info_idx = tray_info_idx
        self.k = k
        self.bed_temp = bed_temp
        self.nozzle_temp_min = nozzle_temp_min
        self.nozzle_temp_max = nozzle_temp_max

    @property 
    def id(self):
        return self._id
    @id.setter 
    def id(self, value):
        self._id = value

    @property 
    def name(self):
        return self._name
    @name.setter 
    def name(self, value):
        self._name = value

    @property 
    def type(self):
        return self._type
    @type.setter 
    def type(self, value):
        self._type = value

    @property 
    def sub_brands(self):
        return self._sub_brands
    @sub_brands.setter 
    def sub_brands(self, value):
        self._sub_brands = value

    @property 
    def color(self):
        return self._color
    @color.setter 
    def color(self, value):
        self._color = value

    @property 
    def tray_info_idx(self):
        return self._tray_info_idx
    @tray_info_idx.setter 
    def tray_info_idx(self, value):
        self._tray_info_idx = value

    @property 
    def k(self):
        return self._k
    @k.setter 
    def k(self, value):
        self._k = value

    @property 
    def bed_temp(self):
        return self._bed_temp
    @bed_temp.setter 
    def bed_temp(self, value):
        self._bed_temp = value

    @property 
    def nozzle_temp_min(self):
        return self._nozzle_temp_min
    @nozzle_temp_min.setter 
    def nozzle_temp_min(self, value):
        self._nozzle_temp_min = value

    @property 
    def nozzle_temp_max(self):
        return self._nozzle_temp_max
    @nozzle_temp_max.setter 
    def nozzle_temp_max(self, value):
        self._nozzle_temp_max = value
