import os
import logging
import sys

import environ
import shutil

import models


class EnvSet:
    def __init__(self):
        # 加载 .env 文件
        self._env = environ.Env(
            DEBUG=(bool, False)
        )

        # 判断是否为开发环境（假设开发环境中存在 requirements.txt 或 setup.py）
        is_dev_env = os.path.exists('requirements.txt') or os.path.exists('setup.py')

        # 设置根目录路径
        if is_dev_env:
            # 开发环境：使用代码项目根目录
            self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            print(f"开发环境：根目录设置为 {self.base_dir}")
        else:
            # 生产环境：优先检查是否为打包后的程序
            if getattr(sys, 'frozen', False):
                # 如果是打包程序，尝试从环境变量或固定路径获取安装目录
                install_dir = os.getenv('3DPRINTERFARM_MANAGER_DIR')  # 可选：通过环境变量动态配置
                if not install_dir:
                    # 默认安装目录（与 setup.py 中的 initial_target_dir 保持一致）
                    install_dir = models.About.default_install_dif
                self.base_dir = install_dir
                print(f"生产环境：根目录设置为安装路径 {self.base_dir}")
            else:
                # 非打包生产环境（如直接运行Python脚本）：使用 Python 的 sys.prefix
                self.base_dir = sys.prefix
                print(f"非打包生产环境：根目录设置为 Python 安装路径 {self.base_dir}")

        self._env_path = os.path.join(self.base_dir, '.env')
        self._env_example_path = os.path.join(self.base_dir, '.env.example')

        # 检查 .env 文件是否存在，若不存在则从 .env.example 拷贝创建
        if not os.path.exists(self._env_path):
            if os.path.exists(self._env_example_path):
                shutil.copyfile(self._env_example_path, self._env_path)
                print(f"从 {self._env_example_path} 创建 {self._env_path}")
            else:
                raise FileNotFoundError(
                    f"未找到 {self._env_path} 或 {self._env_example_path}，请确保至少存在一个文件"
                )

        # 从 .env 文件中读取环境变量
        self._env.read_env(self._env_path)
        self._log_level = int(self._env.get_value('LOG_LEVEL', default=logging.DEBUG))
        self._log_path = f'{self.base_dir}/{self._env.get_value('LOG_PATH', default='./logs')}'
        self._debug = self._env('DEBUG')
        self._wechat_send_url = self._env.get_value("WECHAT_SEND_URL", default="")

    @property
    def log_level(self):
        return self._log_level

    @property
    def log_path(self):
        return self._log_path

    @property
    def debug(self):
        return self._debug

    @property
    def wechat_send_url(self):
        return self._wechat_send_url

    def update_log_path(self, new_path: str):
        """更新日志存放路径"""
        self._log_path = new_path
        self._update_env_file('LOG_PATH', new_path)

    def update_wechat_url(self, new_url: str):
        """更新企业微信通知URL"""
        self._wechat_send_url = new_url
        self._update_env_file('WECHAT_SEND_URL', new_url)

    def _update_env_file(self, key: str, value: str):
        """更新 .env 文件中的配置项"""
        with open(self._env_path, 'r') as f:
            lines = f.readlines()

        with open(self._env_path, 'w') as f:
            for line in lines:
                if line.startswith(f"{key}="):
                    f.write(f"{key}={value}\n")
                else:
                    f.write(line)


env_set = EnvSet()
