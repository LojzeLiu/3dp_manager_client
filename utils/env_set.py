import os
import logging
import environ
from pathlib import Path

# 加载 .env 文件
env = environ.Env(
    DEBUG=(bool, False)
)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = os.path.join(BASE_DIR, '.env')
# 从 .env 文件中读取环境变量
env.read_env(ENV_PATH)


class EnvSet:
    log_level = int(env.get_value('LOG_LEVEL', default=logging.DEBUG))
    log_path = env.get_value('LOG_PATH', default='./logs')
    DEBUG = env('DEBUG')
    WECHAT_SEND_URL = env.get_value("WECHAT_SEND_URL", default="")


env_set = EnvSet()