import json
import os
from lunaryu.utils.logging_config import logger

class Plugin:
    def __init__(self):
        None

    def handle_message(self, message):
        # logger.debug(f'Message: {message}')
        message_dict = json.loads(message)
        if message_dict["post_type"] == "message":
            if message_dict["raw_message"] == 'ping':
                logger.info("收到了一个测试信息")
            if message_dict["raw_message"] == 'force_exit':
                os._exit(1)
        
        return None
