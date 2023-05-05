import json
from datetime import date

def load_pet_info():
    # 펫 정보 JSON 파일 로드
    with open('Pet_info.json', 'r', encoding="utf-8") as f:
        pet_data = json.load(f)
        total_amount = int(pet_data['pet_feed_amount'])

    if pet_data['pet_feed_time_D']:
        amount = round(total_amount/3)
    else:
        amount = round(total_amount/2)
    return amount, pet_data

def add_pet_feed(today):
    # 사료 지급 일지 JSON 파일 로드
    with open('Pet_feed.json', 'r') as f:
        feed_data = json.load(f)
    
    amount, pet_data = load_pet_info()

    # 새로운 feed data 추가
    new_feeding_data = {
        "date": today,
        "feedings": [
            {
                "time": pet_data['pet_feed_time_B'],
                "feed_amount": amount,
                "feed_index" : None,
                "remain_amount": None
            },
            {
                "time": pet_data['pet_feed_time_L'],
                "feed_amount": amount,
                "feed_index" : None,
                "remain_amount": None
            },
            {
                "time": pet_data['pet_feed_time_D'],
                "feed_amount": amount,
                "feed_index" : None,
                "remain_amount": None
            }
        ]
    }
    feed_data['Pet_daily_feed'].append(new_feeding_data)

    # JSON 파일 업데이트.
    with open('Pet_feed.json', 'w') as f:
        json.dump(feed_data, f, indent=4)

def read_today_data():
    # 오늘 날짜를 yyyy-mm-dd 포맷으로 읽어옴
    td = date.today()
    today = f"{td.year}-{str(td.month).zfill(2)}-{str(td.day)}"
    # 사료 지급 일지 JSON 파일 로드
    with open('Pet_feed.json', 'r', encoding="utf-8") as f:
        feed_data = json.load(f)    

    # feed 데이터 업데이트
    feed_dates = [d['date'] for d in feed_data['Pet_daily_feed']]
    try : 
        index = feed_dates.index(today)
    except :
        add_pet_feed(today)
    today_feed = feed_data['Pet_daily_feed'][index]
    return today_feed, feed_data

def edit_pet_feed(feed_list):
    today_feed, feed_data = read_today_data()
    amount, pet_data = load_pet_info()

    list_fff = ['pet_feed_time_B', 'pet_feed_time_L', 'pet_feed_time_D']
    for i in range(3):
        # 사료 지급 시간과 급여량의 변경을 업데이트
        if not today_feed['feedings'][i]["feed_index"] :
            today_feed['feedings'][i]["time"] = pet_data[list_fff[i]]    
            today_feed['feedings'][i]["feed_amount"] = amount
        if feed_list:
            # 남은 양과 급여 여부를 업데이트
            if feed_list[i]:
                today_feed['feedings'][i]['remain_amount'] = feed_list[i]
            elif feed_list[i+3]:
                today_feed['feedings'][i]['feed_index'] = feed_list[i+3]
    # JSON 파일 업데이트.
    with open('Pet_feed.json', 'w') as f:
        json.dump(feed_data, f, indent=4)

if __name__ == "__main__":
    # 인수 -> [아침 잔량, 점심 잔량, 저녁 잔량, 아침 지급, 점심 지급, 저녁 지급]
    edit_pet_feed([0,0,0,0,0,0])