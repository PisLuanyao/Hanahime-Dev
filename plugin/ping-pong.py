from lunaryu.logging_config import logger

from lunaryu.MessageSender import MessageSender


class Plugin:
    def __init__(self):
        self.sender = MessageSender()
        # logger.debug('Test Plugin loaded successfully')
        # print("测试插件加载 (PING-PONG)")

    def handle_message(self, message):
        # logger.debug(f'Message: {message}')
        if message == 'ping':
            # self.sender.send_message('GET', 'http://127.0.0.1:5000')
            data = {"message": "pong"}  # POST请求的数据
            self.sender.post_message('POST', 'http://127.0.0.1:5000', json_data=data)