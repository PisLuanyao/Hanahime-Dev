import os
import shutil
import toml


def LoadConfig(conf_name):
    current_config_path = f'./configs/current_config/{conf_name}.toml'
    default_config_path = f'./configs/default_config/{conf_name}.toml'

    # 检查当前配置文件是否存在
    if not os.path.exists(current_config_path):
        # 如果不存在，从默认配置复制一份
        if os.path.exists(default_config_path):
            shutil.copy(default_config_path, current_config_path)
        else:
            raise FileNotFoundError(f'Neither current nor default config file found for {conf_name}.')

    # 加载配置文件
    return toml.load(current_config_path)
