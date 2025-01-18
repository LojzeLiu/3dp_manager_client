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
    LUCK_START_HOUR = int(env.get_value('LUCK_START_HOUR', default=16))
    LUCK_START_MIN = int(env.get_value('LUCK_START_MIN', default=59))
    LUCK_START_SEC = int(env.get_value('LUCK_START_SEC', default=0))
    LUCK_END_HOUR = int(env.get_value('LUCK_END_HOUR', default=17))
    LUCK_END_MIN = int(env.get_value('LUCK_END_MIN', default=5))
    LUCK_END_SEC = int(env.get_value('LUCK_END_SEC', default=0))
    LUCK_TIME_GAP_SEC = env.get_value('LUCK_TIME_GAP_SEC', default='1')
    ACS_HOST = env.get_value('ACS_HOST', default='https://192.768.50.25:8001')
    SERVER_HOST = env.get_value('SERVER_HOST', default='http://127.0.0.1:8002')

    WECHAT_SEND_URL = env.get_value("WECHAT_SEND_URL", default="")


env_set = EnvSet()

if not bool(env_set.DEBUG):
    env_set.ACS_HOST = 'https://acs.join-all.cn'
    env_set.SERVER_HOST = 'http://47.96.8.227:8000'
