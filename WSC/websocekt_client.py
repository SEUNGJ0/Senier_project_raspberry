import asyncio
import websockets

async def send_message():
    async with websockets.connect('ws://172.20.10.12:88/ws/sensor/') as websocket:
        # Pet_feed Json 파일을 읽어서 서버에게 전송 ()
        with open('Pet_feed.json', 'r', encoding="utf-8") as file:
            pet_feed_data = file.read()
        await websocket.send(pet_feed_data)
        
        # 서버한테 수신받은 데이터
        pet_info = await websocket.recv()
        with open('Pet_info.json', 'w') as file:
            file.write(pet_info)
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_message())

