from hanahime.utils.logging_config import logger


class MessageReceiver:
    def __init__(self):
        self.plugins = []

    def add_plugin(self, plugin):
        self.plugins.append(plugin)

    def process_message(self, message):
        logger.debug(f'Message: {message}')
        for plugin in self.plugins:
            plugin.handle_message(message)
