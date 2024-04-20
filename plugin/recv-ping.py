from lunaryu.logging_config import logger

from lunaryu.MessageSender import MessageSender


class Plugin:
    def __init__(self):
        self.sender = MessageSender()
        # logger.debug('Test Plugin loaded successfully')
        # print("测试插件加 载 (RECV-PONG)")

    def handle_message(self, message):
        # logger.info(f'Message: {message}')
        if message == 'pong':
            logger.info(f'Received message: PONG')
