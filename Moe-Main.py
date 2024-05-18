import asyncio
import json
import os
import websockets

from hanahime.core.ConfigManager import LoadConfig
from hanahime.core.MessageProcessor import message_queue, process_message_from_queue, receiver
from hanahime.core.PluginLoader import PluginLoader as PluginLoader
from hanahime.utils.logging_config import logger

# 加载配置文件
main_config = LoadConfig('config')
# 创建 connected 空集合
connected = set()
# 全局变量，用于指示程序何时停止
stop_app = False


async def websocket_server(websocket, path):
    connected.add(websocket)
    try:
        while True:
            message = await websocket.recv()
            message_dict = json.loads(message)
            meta_event = message_dict["post_type"]
            if meta_event == "meta_event":
                meta_event_type = message_dict["meta_event_type"].upper()
                if meta_event_type == "LIFECYCLE":
                    logger.info(f"Connected - self_id={message_dict['self_id']}")
                    logger.debug(f"{message}")
                elif meta_event_type == "HEARTBEAT":
                    logger.info(f"Heartbeat: self_id={message_dict['self_id']}")
                    logger.trace(f"{message}")
                else:
                    logger.debug(f"{message}")
            else:
                logger.debug(f"\033[41;97m收到:\033[0m {message}")
                await message_queue.put(message)  # 将消息放入异步队列
                # noinspection PyAsyncCall
                asyncio.create_task(process_message_from_queue())  # 在后台处理消息
    except websockets.exceptions.ConnectionClosed:
        logger.debug("Websocket connection closed")
    finally:
        connected.remove(websocket)
        await websocket.close()
        logger.info("理论上WebSocket连接已经全部安全关闭……")
        return None


if __name__ == '__main__':
    plugin_loader = PluginLoader()
    plugins = plugin_loader.load_plugins(os.path.join('.', 'plugin'))
    for plugin in plugins:
        receiver.add_plugin(plugin)  # 将插件添加到MessageReceiver实例中

    start_server = websockets.serve(websocket_server, 'localhost', 10721)

    try:
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        logger.info("发送关闭通知……")
        stop_app = True
        for websocket in list(connected):
            asyncio.get_event_loop().run_until_complete(websocket.close())
        logger.warning("KeyboardInterrupt")
        asyncio.get_event_loop().stop()
