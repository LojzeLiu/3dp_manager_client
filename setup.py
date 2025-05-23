from cx_Freeze import setup, Executable
import models

# 构建选项
build_options = dict(
    packages=["passlib", "asyncio", "pyttsx3", "bs4", "wx", "comtypes"],  # 添加 wx 包
    excludes=[],
    include_files=[
        "resources",
        "assets",
        ".env.example",
        ("lib", "lib"),
    ],
    # 包含 wxPython 的 DLL 文件（根据实际路径调整）
    include_msvcr=True,  # 包含 Microsoft Visual C++ 运行时（部分 wxPython 版本需要）
    build_exe='./build/' + models.About.app_name + "_" + models.About.curr_version
)

# 可执行文件配置
exe = Executable(
    script="main.py",  # 主程序入口文件
    target_name=models.About.app_name,
    icon='resources/imgs/logo.ico',
    shortcut_name=models.About.app_name,
    base="Win32GUI"  # 适用于 GUI 应用
)

# MSI 安装包配置
msi_options = {
    "upgrade_code": "{c7b50a84-8efe-42df-96c2-9dd6cd42f822}",  # 替换为唯一的升级代码（GUID格式）
    "add_to_path": False,  # 是否将程序添加到系统 PATH
    "initial_target_dir": models.About.default_install_dif,
    # 修正快捷方式配置
    "data": {
        "Shortcut": [
            (
                "DesktopShortcut",  # 快捷方式类型
                "DesktopFolder",  # 快捷方式位置（桌面）
                models.About.app_name,  # 快捷方式名称
                "TARGETDIR",  # 目标目录
                "[TARGETDIR]%s.exe" % models.About.app_name,  # 目标路径
                None,  # 工作目录（可选）
                None,  # 参数（可选）
                None,  # 描述（可选）
                None,  # 热键（可选）
                None,  # 图标路径（可选）
                None,  # 图标索引（可选）
                None,  # 显示方式（可选）
            ),
            # 新增：开始菜单快捷方式
            (
                "StartMenuShortcut",  # 快捷方式类型
                "ProgramMenuFolder",  # 快捷方式位置（开始菜单）
                models.About.app_name,  # 快捷方式名称
                "TARGETDIR",  # 目标目录
                "[TARGETDIR]%s.exe" % models.About.app_name,  # 目标路径
                None,  # 工作目录（可选）
                None,  # 参数（可选）
                None,  # 描述（可选）
                None,  # 热键（可选）
                None,  # 图标路径（可选）
                None,  # 图标索引（可选）
                None,  # 显示方式（可选）
            )
        ]
    }
}

setup(
    name=models.About.app_name,  # 应用名称
    version=models.About.curr_version,
    description="3D 打印机集群管理程序",
    options={
        "build_exe": build_options,  # 构建可执行文件的选项
        "bdist_msi": msi_options,  # 生成 MSI 安装包的选项
    },
    executables=[exe],
)