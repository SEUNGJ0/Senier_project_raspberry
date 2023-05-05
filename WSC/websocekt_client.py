import asyncio
import websockets

async def send_message():
<<<<<<< HEAD
    async with websockets.connect('ws://192.168.1.182:88/ws/sensor/') as websocket:
=======
    async with websockets.connect('ws://192.168.1.183:81/ws/sensor/') as websocket:
>>>>>>> daeadeff6ef961fe8f5e4d8d3c48c13895733e3f
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

