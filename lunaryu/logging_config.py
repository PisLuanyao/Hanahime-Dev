from loguru import logger
import datetime

# 配置日志记录器
log_file = f"./logs/{datetime.datetime.now():%b-%d-%Y}.log"

logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)
logger.add(log_file, rotation="128 MB", level="INFO", format=logger_format)

logger = logger
