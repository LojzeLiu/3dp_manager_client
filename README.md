# 3D打印机集群管理系统
> 一款开源免费的3D打印机集群管理软件，使用Python开发。在打印机处于局域网模式或者农场模式下，任具备强语音提醒、远程提醒、统一操作等功能，为你的农场降本增效。
# 功能亮点
1. 多台拓竹打印机统一监看、提醒、管理（简单管理）；
2. 兼容**拓竹农场管家**，扩展**拓竹农场管家**功能；
3. 具备语音和远程提醒功能，在打印机意外停止时，可第一时间干预处理，减少暂停时间；
4. 集群控制打印机灯光，下班或无人时减少电能消耗；
5. 中文界面，操作友好；
6. 开源免费，一件安装即可使用。

## 未来功能
1. 远程监看、管理、安排生产；
2. 接入更多品牌、型号；
3. 打印机务管理；
4. 多语言支持；
5. 打印机扩展设备接入统一管理；
6. 打印机分组管理。

# 兼容设备（已测试）
1. 拓竹 A1；
2. 拓竹 A1 Mini；
3. 拓竹 P1S。

# 使用教程
## 系统与网络要求
1. Windows10或更高版本操作系统；
2. 使用X86指令集64位处理器的电脑或平板；
3. 打印机使用2.4G WIFI接入局域网；
4. 打印机、**3D打印机集群管理系统**、**拓竹农场管家**需要部署在同一个局域网中，或三者可基于IP地址通信（如同路由器下的不同子网）；
5. **3D打印机集群管理系统**、**拓竹农场管家客户端**需要具备公网访问能力。
## 打印机固件要求
1. Bambu Lab P1P/P1S: 请更新至V01.07.00.00 或之后的版本 
2. Bambu lab A1/A1mini: 请更新至V01.04.00.00 或之后的版本
## 安装**拓竹农场管家**（非必须）
> **拓竹农场管家** 安装教程请[点击这里查看](https://wiki.bambulab.com/zh/software/bambu-farm-manager)，并按照教程完成安装。建议将**拓竹农场管家**和**3D打印机集群管理系统**安装在一台电脑上。
## 安装 **3D打印机集群管理系统**
1. [点击这里 （GitHub）](https://github.com/LojzeLiu/3dp_manager_client/releases)下载最新版本（无法访问[点击这里（码云）](https://gitee.com/lojzeliu/3dp_manager_client/releases/)下载）；
2. 双击启动安装程序，按提示选择安装路径（路径不能包含英文）；
3. 接下来一直点击下一步即可完成安装。

## 设置远程通知
> 目前远程通知使用的是企业微信群的方式通知，这是目前我能找到成本最低的（金钱成本为0），通知效率较高的一种方法。如果你有更好的方法，可以[点击这里](https://gitee.com/lojzeliu/3dp_manager_client/issues)提交你的建议。

1. 下载注册企业微信（无需付费认证）；
2. 创建群聊，至少选择2名要需要接收通知的成员（必须是内部群）；

 <img height="600" src="https://s2.loli.net/2025/05/24/Cl8WfmoKLdRG5D7.jpg" width="300"/>

3. 点击右上角三个点，进入群管理；
4. 点击**群机器人**；

 <a href="https://sm.ms/image/CrOmcbADywPd6Yh" target="_blank"><img height="600" width="300" src="https://s2.loli.net/2025/05/24/CrOmcbADywPd6Yh.jpg" ></a>

5. 点击**添加机器人**；

<a href="https://sm.ms/image/fIjGT7BJEbSiVRK" target="_blank"><img height="600" width="300" src="https://s2.loli.net/2025/05/24/fIjGT7BJEbSiVRK.jpg" ></a>

6. 点击右上角新建；

<a href="https://sm.ms/image/ZEr8xiOWoV34fRm" target="_blank"><img height="600" width="300"  src="https://s2.loli.net/2025/05/24/ZEr8xiOWoV34fRm.jpg" ></a>

7. 输入机器人名字，点击添加；

<a href="https://sm.ms/image/ZLDPK5CT2S3gwAx" target="_blank"><img height="600" width="300" src="https://s2.loli.net/2025/05/24/ZLDPK5CT2S3gwAx.jpg" ></a>

8. 点击复制 **Webhook地址**；

<a href="https://sm.ms/image/1uahfjSkp6sMXOC" target="_blank"><img height="600" width="300" src="https://s2.loli.net/2025/05/24/1uahfjSkp6sMXOC.jpg" ></a>

9. 在 **3D打印机集群管理系统** 主窗口，点击右上角设置图标；

![image.png](https://s2.loli.net/2025/05/24/TYUkvsL1gO2icDn.png)

10. 在弹出窗口点击 **通知设置**，在企业微信通知URL输入栏，粘贴刚刚复制的**Webhook地址**；

![image.png](https://s2.loli.net/2025/05/24/c4PEN2YgzCxhr5w.png)

11. 点击测试通知，查看企业微信群消息，如果收到如下提示，则代表配置成功；

![image.png](https://s2.loli.net/2025/05/24/MRWVw2Gxj9mAQPK.png)


<a href="https://sm.ms/image/RLHuBIYbjZd7TnS" target="_blank"><img height="600" src="https://s2.loli.net/2025/05/24/RLHuBIYbjZd7TnS.png" ></a>

12. 点击保存设置，关闭软件设置窗口即可。

## 添加打印机
1. 点击下图所示图标，打开打印机管理窗口；

![image.png](https://s2.loli.net/2025/05/24/4GKU9Zy2mADxeuB.png)

2. 点击下图所示按钮，添加打印机；

![image.png](https://s2.loli.net/2025/05/24/q2hEArnYT5cDCp4.png)
3. 输入名称（名称建议可以清晰区分每一台打印机）、IP 地址、访问码、机器码，点击OK；

![image.png](https://s2.loli.net/2025/05/24/7YzNpkAfBcHMXPj.png)

4. IP 地址和机器码可以从**拓竹农场管家客户端**复制粘贴；

![image.png](https://s2.loli.net/2025/05/24/KgMjXyO4qPSG8ch.png)


![image.png](https://s2.loli.net/2025/05/24/7vB4o3t26qi5W1R.png)


5. 访问码需从打印机获取，方法见获取访问码一章；
6. 完成添加打印机后，点击打印机管理窗口最下端的关闭按钮，关闭打印机管理窗口后，程序会自动加载打印机，加载过程较慢（打印机越多，越慢）；

## 删除打印机
1. 点击下图所示图标，打开打印机管理窗口；
![image.png](https://s2.loli.net/2025/05/24/4GKU9Zy2mADxeuB.png)
2. 右键选择要删除的打印机，点击删除选项，即可删除打印机。

![image.png](https://s2.loli.net/2025/05/24/O9DqYu23mEz5UXx.png)

## 修改打印机信息
1. 点击下图所示图标，打开打印机管理窗口；

![image.png](https://s2.loli.net/2025/05/24/4GKU9Zy2mADxeuB.png)

2. 右键选择要修改的打印机，点击修改选项；

![image.png](https://s2.loli.net/2025/05/24/X6bpSPjgAlm4wU9.png)

3. 在弹出窗口修改信息，完成修改后，点击ok按钮即可保存修改信息。

![image.png](https://s2.loli.net/2025/05/24/fDT8d3empbJQqtH.png)

## 查看打印机详情
1. 点击要查看的打印机标签（点击空白处），即可弹出详情窗口；

![image.png](https://s2.loli.net/2025/05/24/faI5lehcF2TEU3O.png)

2. 此窗口可以查看：打印机序列号、IP地址、WiFi强度、设备状态、耗材信息、运行实况、摄像头画面；
![printer_info.jpg](https://s2.loli.net/2025/05/24/qJtNakZ2hCwcMnD.jpg)
3. 下滑窗口，可查看摄像头内容。
![](https://s2.loli.net/2025/05/24/OpeNKQ8a6PTvMDV.png)

## 更多便捷功能
1. 点击顶部操作条的灯光图标，可以统一控制LED灯光开关；
2. 点击打印机标签处的灯光图标，可以单独控制指定打印机的LED灯光；
3. 点击下图所示图标，可以切换软件全屏状态；
4. 点击下图所示图标，可以关闭语音通知；
![image.png](https://s2.loli.net/2025/05/24/1e8vhK9NaLHAcPQ.png)

## 获取打印机访问码
### P1S
![image.png](https://s2.loli.net/2025/05/24/WkYmfxtUrszHq1l.png)

![image.png](https://s2.loli.net/2025/05/24/8XrTRKUhENviJSa.png)

### A1 & A1 Mini
![image.png](https://s2.loli.net/2025/05/24/6Va1TYpJn8UNACj.png)

![image.png](https://s2.loli.net/2025/05/24/giUEadH95bFmpM6.png)

![image.png](https://s2.loli.net/2025/05/24/pJvh5GjANUE7sWg.png)
# 相关逻辑说明
## 语音通知开关
1. 当语音通知开启后，程序接收到一个打印机事件（需要通知的），会阻塞等待用户操作，在此期间，语音会滚动播放。直到用户操作后，才会处理下一个事件。该模式适合设备旁有人时开启；
2. 当语音通知关闭后，程序接收到一个打印机事件（需要通知的），不会阻塞等待，会直接发生远程通知，并且不会有语音播放，并立即处理下一个事件。该模式适合设备旁无人时关闭语音通知。
## 灯光开关
1. 当点击顶部统一灯光开关时，程序会依次向每台打印机发生关灯指令；
2. 每台设备标签上的灯光控制按钮，会在接收到打印机的灯光状态切换指令后，切换灯光图标到对应状态，在此期间，按钮是禁止点击的；
3. 单独操作指定设备的灯光，逻辑和上面所说的相似，所以图标状态切换会有一定的延迟。

# 关于开发
## 环境需求
1. python : 3.12;
2. 其他依赖见：requirements.txt
## 安装依赖
```shell
cd 3dp_manager_client
pip install -r requirements.txt 
```
## 测试运行
```shell
python main.py
```
## 打包构建
```shell
python setup.py bdist_msi
```

# 问题提交

请[点击这里](https://gitee.com/lojzeliu/3dp_manager_client/issues)，提交你的问题。

# 使用开源项目
1. [bambu-printer-manager](https://github.com/synman/bambu-printer-manager)