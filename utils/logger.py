import logging
import os
from logging import handlers

from utils.env_set import env_set

log_base_path = env_set.log_path
if not os.path.exists(log_base_path):
    os.mkdir(log_base_path)

log_path = f'{log_base_path}/3dpm.log'

logger = logging.getLogger('3dpm')
logger.setLevel(level=logging.DEBUG)

formatter = logging.Formatter('%(asctime)s-[%(filename)s-%(lineno)d]-[%(funcName)s]-[%(levelname)s]: %(message)s')
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(level=logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(env_set.log_level)
stream_handler.setFormatter(formatter)

time_rotating_file_handler = handlers.TimedRotatingFileHandler(filename=log_path, when='D')
time_rotating_file_handler.setLevel(env_set.log_level)
time_rotating_file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.addHandler(time_rotating_file_handler)
