import asyncio
import websockets
import json
import os

async def hello():
    url = "ws://192.168.226.43:4000"
    #async with websockets.connect(url) as websocket:
    websocket = await websockets.connect(url)    
    name = '["boardInfo",{"type":"device","name":"testname","OK":true,"msg":"Success","deviceType":"identifier"}]'
    await websocket.send(name)
    print(f">{name}")
    try:
        response = await websocket.recv()
        print(f"<{response}")
    except:
        print("Reconnecting")
        websocket = await websockets.connect(url)

#asyncio.get_event_loop().run_until_complete(hello())

asyncio.run(hello())
