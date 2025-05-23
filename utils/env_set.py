import os
import logging
import environ
import shutil


class EnvSet:
    def __init__(self):
        # 加载 .env 文件
        self._env = environ.Env(
            DEBUG=(bool, False)
        )
        self._base_dir = './'
        self._env_path = os.path.join(self._base_dir, '.env')
        self._env_example_path = os.path.join(self._base_dir, '.env.example')

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
        self._log_path = self._env.get_value('LOG_PATH', default='./logs')
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