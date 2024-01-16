import os
import importlib.util

from lunaryu.logging_config import logger


class PluginLoader:
    def load_plugins(self, plugin_dir):
        plugins = []
        for file_name in os.listdir(plugin_dir):
            if file_name.endswith('.py'):
                plugin_name = file_name[:-3]
                logger.debug(f'Loading files: {plugin_name}')
                plugin_path = os.path.join(plugin_dir, file_name)
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'Plugin'):
                    logger.info(f'Successfully loaded file: {plugin_name}')
                    plugins.append(module.Plugin())
        return plugins
