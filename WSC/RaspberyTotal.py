from WSC import feedupdate, websocekt_client
import asyncio
import time
def WSC_main():
    while True:
        try:
            asyncio.get_event_loop().run_until_complete(websocekt_client.send_message())
        except:
            print("서버 통신 오류")
        feedupdate.edit_pet_feed(None)
        time.sleep(5)

if __name__ == "__main__":
    WSC_main()
        
        
    