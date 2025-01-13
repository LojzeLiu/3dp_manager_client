from cx_Freeze import setup, Executable

import models

build_options = dict(packages=["passlib", "asyncio","pyttsx3","bs4"], excludes=[],
                     include_files=[
                         "resources",
                         ".env",
                         "bambu.db",
                     ])

# 注意：将 'YourApp' 替换为你的应用名称
exe = Executable(
    script="main.py",  # 将 'your_app.py' 替换为你的主应用文件
    target_name=models.About.app_name,
    icon='resources/imgs/logo.ico',
    shortcut_name=models.About.app_name,
    base="Win32GUI"
)

setup(
    name="3DP",  # 将 'YourApp' 替换为你的应用名称
    version=models.About.curr_version,
    description="3D 打印机集群管理程序",
    options=dict(build_exe=build_options),
    executables=[exe],
)
