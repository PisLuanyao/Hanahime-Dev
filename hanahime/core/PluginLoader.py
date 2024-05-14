import os
import importlib.util
from hanahime.utils.logging_config import logger


class PluginLoader:
    def load_plugins(self, plugin_dir):
        plugins = []
        loaded_plugin_names = []  # 新增一个列表来记录成功加载的插件名称
        error_plugin_names = []  # 新增一个列表来记录错误的插件名称
        for entry in os.scandir(plugin_dir):
            if entry.name == '__pycache__':  # 检查是否为__pycache__文件夹
                continue  # 如果是，跳过
            try:
                if entry.is_dir():
                    index_path = os.path.join(entry.path, 'index.py')
                    if os.path.isfile(index_path):
                        plugin_name = entry.name
                        logger.debug(f'[v2模式] 加载插件 {plugin_name}')
                        plugin = self.load_plugin(index_path, plugin_name)
                        if plugin:
                            plugins.append(plugin)
                            loaded_plugin_names.append(plugin_name)
                    else:
                        error_plugin_names.append(entry.name)  # 如果没有index.py，添加到错误列表
                        logger.info(
                            f'[v2模式] 文件夹 \u001b[33m{entry.name}\u001b[0m \u001b[97m中缺少 index.py 无法加载插件')
                elif entry.is_file() and entry.name.endswith('.py'):
                    plugin_name = entry.name[:-3]
                    logger.debug(f'[v1模式] 加载插件 {plugin_name}')
                    plugin = self.load_plugin(entry.path, plugin_name)
                    if plugin:
                        plugins.append(plugin)
                        loaded_plugin_names.append(plugin_name)
            except Exception as e:
                error_plugin_names.append(entry.name)  # 添加出错的插件名称到列表
                logger.info(f'加载插件 \u001b[33m{entry.path}\u001b[0m \u001b[97m时发生错误: \u001b[31m{e}')
        # 在遍历结束后打印成功和错误的插件列表
        logger.success(f'有 {len(loaded_plugin_names)} 个插件被成功加载\nSuccessfully loaded: {loaded_plugin_names} ')
        if error_plugin_names:  # 如果有错误的插件
            logger.warning(f'有 {len(error_plugin_names)} 个插件加载失败\nFailed to load: {error_plugin_names} ')
        return plugins

    def load_plugin(self, path, name):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'Plugin'):
            return module.Plugin()
        return None
