import datetime

from loguru import logger
from sys import stdout
from .LoadBasicConfig import _LoadConfig as load_config

# 配置日志记录器
log_file = f"./logs/{datetime.datetime.now():%b-%d-%Y}.log"

logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

logger.remove()  # 先移除，再添加回来

logging_config = load_config('logging')
disable_logfile = logging_config.get('logfile', {}).get('disable_logfile', False)
if not disable_logfile:
    rotation = f"{logging_config.get('logfile', {}).get('logfile_size', 16)} MB"
    logfile_level = logging_config.get('logfile', {}).get('logfile_level', 'INFO')
    logger.add(log_file, rotation=rotation, level=logfile_level, format=logger_format)
else:
    print("⚠⚠⚠ 已禁用日志文件, 这是不推荐的做法 ⚠⚠⚠")

stdout_level = logging_config.get('console', {}).get('logfile_level', 'DEBUG')
logger.add(stdout, level=stdout_level, format=logger_format)

logger = logger
