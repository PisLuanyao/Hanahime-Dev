# 创建一个MessageReceiver实例
import asyncio

from hanahime.core.MessageReceiver import MessageReceiver
from hanahime.utils.logging_config import logger

receiver = MessageReceiver()
# 创建一个消息队列
message_queue = asyncio.Queue()


# @logger.catch
async def process_message_from_queue():
    # global stop_app
    stop_app = bool(0)
    while not stop_app or not message_queue.empty():
        message = await message_queue.get()
        if message is None:  # 如果消息是None，代表是退出信号
            break
        receiver.process_message(message)  # 使用MessageReceiver实例处理消息
