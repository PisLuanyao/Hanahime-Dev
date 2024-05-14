import os
import shutil
import toml

from hanahime.utils.logging_config import logger
from hanahime.other.datetime import StrTime


def LoadConfig(conf_name):
    logger.debug(f'Loading Config: {conf_name}')
    current_config_path = f'./configs/current_config/{conf_name}.toml'
    default_config_path = f'./configs/default_config/{conf_name}.toml'

    # 检查当前配置文件是否存在
    if not os.path.exists(current_config_path):
        # 如果不存在，从默认配置复制一份
        if os.path.exists(default_config_path):
            shutil.copy(default_config_path, current_config_path)
            logger.warning(
                f'Current configuration not found, reverted from default configuration file: {conf_name}.toml')
        else:
            logger.critical(f'Configuration file not found: {conf_name}.toml')
            # raise FileNotFoundError(f'Neither current nor default config file found for {conf_name}.')

    # 加载配置文件
    config_file_exists = os.path.exists(current_config_path)
    if config_file_exists:
        try:
            loaded_config = toml.load(current_config_path)
            logger.info(f'Loaded Config: {conf_name}')
            return loaded_config
        except toml.TomlDecodeError:
            logger.warning('TomlDecodeError - The configuration file may be corrupted')
            logger.info('Empty dictionary has been returned!')
            return {}
    else:
        logger.info('Empty dictionary has been returned!')
        return {}


def RestoreConfig(conf_name):
    logger.debug(f'Restoring Config: {conf_name}')
    current_config_path = f'./configs/current_config/{conf_name}.toml'
    backup_config_dir = f'./configs/current_config/backups'
    backup_config_path = os.path.join(backup_config_dir, f'{conf_name}.toml-{StrTime(_fs_friendly=True)}.bak')
    default_config_path = f'./configs/default_config/{conf_name}.toml'

    # 确保备份文件夹存在
    os.makedirs(backup_config_dir, exist_ok=True)

    if os.path.exists(current_config_path):  # 尝试还原配置文件
        os.makedirs(backup_config_dir, exist_ok=True)
        shutil.copy(current_config_path, backup_config_path)
        shutil.copy(default_config_path, current_config_path)
        logger.info(f'Reverted from default configuration file: {conf_name}.toml')
    else:
        logger.critical(f'找不到文件: {conf_name}.toml')
        raise FileNotFoundError(f'Configuration file does not exist: {conf_name}.')


def LoadConfigByCustomPath(conf_name, conf_path):
    None


def WriteSysConfig(conf_name):
    None
