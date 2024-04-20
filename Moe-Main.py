import asyncio
import json
import websockets
from lunaryu.ConfigManager import LoadConfig as load_config
from lunaryu.MessageReceiver import MessageReceiver
from lunaryu.PluginLoader import PluginLoader
from lunaryu.logging_config import logger
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import multiprocessing

# 加载配置文件
config = load_config('config')

# 创建一个MessageReceiver实例
receiver = MessageReceiver()
# 创建一个消息队列
message_queue = Queue()
# 创建一个线程池
max_workers = config.get('max_workers', {}).get('threads', '2')
max_workers = multiprocessing.cpu_count() * 4 if max_workers == 'default' else int(max_workers)
logger.debug(f"创建线程池: {max_workers}线程")
thread_pool = ThreadPoolExecutor(max_workers=max_workers)


async def process_message_from_queue():
    while True:
        message = await asyncio.get_event_loop().run_in_executor(thread_pool, message_queue.get)
        if message is None:  # 如果消息是None，代表是退出信号
            break
        receiver.process_message(message)  # 使用MessageReceiver实例处理消息


async def websocket_server(websocket, path):
    while True:
        message = await websocket.recv()
        message_dict = json.loads(message)
        meta_event = message_dict["post_type"]
        if meta_event == "meta_event":
            meta_event_type = message_dict["meta_event_type"].upper()
            if meta_event_type == "LIFECYCLE":
                logger.debug("Connected")
                logger.debug(f"{message}")
            elif meta_event_type == "HEARTBEAT":
                logger.debug(f"Heartbeat: {message}")
            else:
                logger.debug(f"{message}")
        else:
            message_queue.put(message)  # 将消息放入队列
            asyncio.create_task(process_message_from_queue())  # 在后台处理消息
        await websocket.send('Message received')


if __name__ == '__main__':
    plugin_loader = PluginLoader()
    plugins = plugin_loader.load_plugins('./plugin')
    for plugin in plugins:
        receiver.add_plugin(plugin)  # 将插件添加到MessageReceiver实例中

    start_server = websockets.serve(websocket_server, 'localhost', 8760)

    try:
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        logger.error("KeyboardInterrupt")
