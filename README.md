
## 打包构建
```shell
python setup.py build
```


## 相关参数记录

### BambuPrinter 打印机信息解释

```aiignore
----------
* _mqtt_client_thread: `PRIVATE` MQTT 客户端线程的线程句柄（私有）
* _watchdog_thread: `PRIVATE` 看门狗线程的线程句柄（私有）
* _internalExcepton: `READ ONLY` 如果发生故障，返回底层的 `Exception` 对象（只读）
* _lastMessageTime: `READ ONLY` 从打印机收到更新的最后时间的时间戳（秒）（只读）
* _recent_update: `READ ONLY` 表示最近已处理来自打印机的消息（只读）
* _config: `READ/WRITE` 与此实例关联的 `bambuconfig.BambuConfig` 配置对象（可读写）
* _state: `READ/WRITE` `bambutools.PrinterState` 枚举，报告与打印机的连接健康状况/状态（可读写）
* _client: `READ ONLY` 提供对底层 `paho.mqtt.client` 库的访问（只读）
* _on_update: `READ/WRITE` 用于推送更新的回调。包括对 `BambuPrinter` 的自引用作为参数（可读写）
* _bed_temp: `READ ONLY` 当前打印机床温度（只读）
* _bed_temp_target: `READ/WRITE` 打印机的目标床温度（可读写）
* _bed_temp_target_time: `READ ONLY` 上次设置目标床温度的时间戳（只读）
* _tool_temp: `READ ONLY` 当前打印机工具温度（只读）
* _tool_temp_target: `READ/WRITE` 打印机的目标工具温度（可读写）
* _tool_temp_target_time: `READ ONLY` 上次设置目标工具温度的时间戳（只读）
* _chamber_temp `READ/WRITE` 当前未集成，但可用作外部室的占位符（可读写）
* _chamber_temp_target `READ/WRITE` 当前未集成，但可用作外部室目标温度的占位符（可读写）
* _chamber_temp_target_time: `READ ONLY` 上次设置目标室温度的时间戳（只读）
* _fan_gear `READ ONLY` 组合风扇的报告值。可通过位移操作获得各个风扇的速度（只读）
* _heat_break_fan_speed `READ_ONLY` 热断风扇（加热块风扇）的速度百分比（只读）
* _fan_speed `READ ONLY` 零件冷却风扇的速度百分比（只读）
* _fan_speed_target `READ/WRITE` 零件冷却风扇的目标速度百分比（可读写）
* _fan_speed_target_time: `READ ONLY` 上次设置目标风扇速度的时间戳（只读）
* _light_state `READ/WRITE` 表示工作灯状态的布尔值（可读写）
* _wifi_signal `READ ONLY` 打印机当前的 Wi-Fi 信号强度（只读）
* _speed_level `READ/WRITE` 系统打印速度（1=静音，2=标准，3=运动，4=极速）（可读写）
* _gcode_state `READ ONLY` 报告工作状态（失败/运行/暂停/空闲/完成）的状态（只读）
* _gcode_file `READ ONLY` 当前或最后打印的 gcode 文件名（只读）
* _3mf_file `READ ONLY` 当前正在打印的 3mf 文件名（只读）
* _plate_num `READ ONLY` 当前 3mf 文件选定的平板号（只读）
* _subtask_name `READ ONLY` 活动子任务的名称（只读）
* _print_type `READ ONLY` 不完全确定。在没有活动作业时报告“空闲”（只读）
* _percent_complete `READ ONLY` 当前活动作业的完成百分比（只读）
* _time_remaining `READ ONLY` 活动作业预估剩余分钟数（只读）
* _start_time `READ ONLY` 最后一个（或当前）活动作业的开始时间（分钟时间戳）（只读）
* _elapsed_time `READ ONLY` 最后一个（或当前）活动作业的已过时间（分钟）（只读）
* _layer_count `READ ONLY` 当前活动作业的总层数（只读）
* _current_layer `READ ONLY` 当前活动作业正在打印的当前层（只读）
* _current_stage `READ ONLY` 映射到 `bambutools.parseStage`（只读）
* _current_stage_text `READ ONLY` 解析 `current_stage` 值（只读）
* _spools `READ ONLY` 已加载的所有线轴的元组。可包含多达 5 个 `BambuSpool` 对象（只读）
* _target_spool `READ_ONLY` 打印机正在转换到的线轴号（`0-3`=AMS, `254`=外部, `255`=无）（只读）
* _active_spool `READ_ONLY` 打印机当前使用的线轴号（`0-3`=AMS, `254`=外部, `255`=无）（只读）
* _spool_state `READ ONLY` 表示线轴是已装载、装载中、未装载还是卸载中（只读）
* _ams_status `READ ONLY` AMS 的位编码状态（当前未使用）（只读）
* _ams_exists `READ ONLY` 表示检测到 AMS 的布尔值（只读）
* _ams_rfid_status `READ ONLY` AMS RFID 读取器的位编码状态（当前未使用）（只读）
* _sdcard_contents `READ ONLY` SDCard 上所有文件的 `dict`（json）值（需要首先调用 `get_sdcard_contents`）（只读）
* _sdcard_3mf_files `READ ONLY` SDCard 上所有 `.3mf` 文件的 `dict`（json）值（需要首先调用 `get_sdcard_3mf_files`）（只读）
* _hms_data `READ ONLY` 任何活动 hms 代码的 `dict`（json）值，如果是已知代码，则附带描述（只读）
* _hms_message `READ ONLY` 所有 hms_data `desc` 字段连接成的单个字符串，便于使用（只读）
* _print_type `READ ONLY` 可为 `cloud` 或 `local`（只读）
* _skipped_objects `READ ONLY` 已被跳过/取消的对象数组（只读）

```

## 参考资料

[bambu-printer-manager](https://synman.github.io/bambu-printer-manager/)