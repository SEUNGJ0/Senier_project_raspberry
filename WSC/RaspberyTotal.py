import feedupdate
import websocekt_client
import asyncio
import schedule
import time
from datetime import datetime as date

def main():
    now = date.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time)
    
    amount, pet_data = feedupdate.load_pet_info()
    epf_args_list = []
    if current_time == "00:00:00":
        epf_args_list = [0,0,0,0,0,0]
    elif current_time == pet_data['pet_feed_time_B']:
        epf_args_list = [0,0,0,1,0,0]
    elif current_time == pet_data['pet_feed_time_L']:
        epf_args_list = [0,0,0,0,1,0]
    elif current_time == pet_data['pet_feed_time_D']:
        epf_args_list = [0,0,0,0,0,1]

    if epf_args_list:
        feedupdate.edit_pet_feed(epf_args_list)
    else:
        feedupdate.edit_pet_feed([0,0,0,0,0,0])

    # websocekt_client.send_message()
    asyncio.get_event_loop().run_until_complete(websocekt_client.send_message())

if __name__ == "__main__":
    while(True):
        main()
        time.sleep(1)
        
    