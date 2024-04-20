import asyncio
import json

import websockets

from lunaryu.MessageReceiver import MessageReceiver
from lunaryu.PluginLoader import PluginLoader
from lunaryu.logging_config import logger

receiver = MessageReceiver()  # 创建一个MessageReceiver实例


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
                # receiver.process_message(message)  # 使用之前创建的MessageReceiver实例处理消息
                logger.debug(f"Heartbeat: {message}")
            else:
                # receiver.process_message(message)  # 使用之前创建的MessageReceiver实例处理消息
                logger.debug(f"{message}")
        else:
            message = message
            receiver.process_message(message)  # 使用之前创建的MessageReceiver实例处理消息
        # receiver.process_message(message)  # 使用之前创建的MessageReceiver实例处理消息
        await websocket.send('Message received')


if __name__ == '__main__':
    plugin_loader = PluginLoader()
    plugins = plugin_loader.load_plugins('./plugin')
    for plugin in plugins:
        receiver.add_plugin(plugin)  # 将插件添加到之前创建的MessageReceiver实例中

    start_server = websockets.serve(websocket_server, 'localhost', 8760)

    try:
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        logger.warning("KeyboardInterrupt")