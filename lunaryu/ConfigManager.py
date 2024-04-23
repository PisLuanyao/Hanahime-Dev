import os
import shutil
import toml

from lunaryu.logging_config import logger


def LoadConfig(conf_name):
    logger.debug(f'Loading Config: {conf_name}')
    current_config_path = f'./configs/current_config/{conf_name}.toml'
    default_config_path = f'./configs/default_config/{conf_name}.toml'

    # 检查当前配置文件是否存在
    if not os.path.exists(current_config_path):
        # 如果不存在，从默认配置复制一份
        if os.path.exists(default_config_path):
            shutil.copy(default_config_path, current_config_path)
            logger.warning(f'Current configuration not found, reverted from default configuration file: {conf_name}.toml')
        else:
            logger.critical(f'Configuration file not found: {conf_name}.toml')
            raise FileNotFoundError(f'Neither current nor default config file found for {conf_name}.')

    # 加载配置文件
    logger.info(f'Loaded Config: {conf_name}')
    return toml.load(current_config_path)

def LoadConfigByCustomPath(conf_name, conf_path):
    None

def WriteSysConfig(conf_name):
    None
