from WSC import feedupdate, websocekt_client
import asyncio
import time
from datetime import datetime as date

def WSC_main():
    while True:
        now = date.now()
        current_time = now.strftime("%H:%M:%S")        

        amount, pet_data = feedupdate.load_pet_info()
        # epf_args_list[0:3] -> 남은 사료량
        # epf_args_list[3:6] -> 사료 지급 여부
        epf_args_list = [0, 0, 0, 0, 0, 0]
        if current_time == pet_data['pet_feed_time_B']:
            epf_args_list[3] = 1
        elif current_time == pet_data['pet_feed_time_L']:
            epf_args_list[4] = 1
        elif current_time == pet_data['pet_feed_time_D']:
            epf_args_list[5] = 1

        feedupdate.edit_pet_feed(epf_args_list)
        try:
            asyncio.get_event_loop().run_until_complete(websocekt_client.send_message())
        except:
            print("서버 통신 오류")
        time.sleep(1)

if __name__ == "__main__":
    WSC_main()
        
        
    