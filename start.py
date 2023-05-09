import time, multiprocessing, threading
from Motor.stepmoter_set import StepperMotor
from HX711.RoadCellOutput import Massdetection
import LCD.LCD_Output as lcd
from WSC.feedupdate import load_pet_info,read_today_data,edit_pet_feed
from WSC.RaspberyTotal import WSC_main
from collections import OrderedDict

file_data = OrderedDict()
STM = StepperMotor()
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

def feed_output(amount):
    lcd.lcd_init() 
    feedmass = Massdetection()
    lcd.lcd_string(f"Target : {amount}g.", LCD_LINE_1)

    STM.run_on()
    while(True):
        lcd.lcd_string(f"Measured : {feedmass.weight_input()}g", LCD_LINE_2)
        time.sleep(0.1)
        if feedmass.weight_input() >= amount:
            STM.run_off()
            print(feedmass.weight_input())
            return feedmass.weight_input()

def time_add(time_str_list):
    # 시간과 분을 분리하고 정수형으로 변환
    new_time_str_list = []
    for time_str in time_str_list:
        hours, minutes = map(int, time_str.split(':'))

        # 30분 추가
        hours, minutes = divmod(hours*60 + minutes + 30, 60)

        # 시간을 24로 나눈 나머지로 설정
        hours %= 24

        # 새로운 시간을 문자열로 출력
        new_time_str = f"{hours:02d}:{minutes:02d}"
        new_time_str_list.append(new_time_str)
    return new_time_str_list

def main():
    # LCD 초기화
    lcd.lcd_init()
    while True:
        # 사용자가 설정한 펫 정보데이터와 하루 지급 사료량 읽어옴
        amount, pet_data = load_pet_info()
        CrtTime = time.strftime('%H:%M')
        
        # 현재 시각과 지정된 시간 대조 조건문 
        feed_time_list = [pet_data['pet_feed_time_B'], pet_data['pet_feed_time_L'], pet_data['pet_feed_time_D']]
        feed_time_add_list = time_add(feed_time_list)
        epf_args_list = [0, 0, 0, 0, 0, 0]
        today_feed, feed_data = read_today_data()
        if CrtTime in feed_time_list:
            feed_index = int(feed_time_list.index(CrtTime))
            if not today_feed['feedings'][feed_index]["feed_index"]:
                given_amount = feed_output(amount)
                lcd.lcd_string("Done!!", LCD_LINE_1)
                lcd.lcd_string(f"Given: {given_amount}g", LCD_LINE_2)
                epf_args_list[feed_index+3] = int(given_amount)
                edit_pet_feed(epf_args_list)
                time.sleep(5)
                                
        else:
            lcd.lcd_string("Current Time", LCD_LINE_1)
            lcd.lcd_string(CrtTime, LCD_LINE_2)

        # Refresh 빈도 설정
        time.sleep(5)

if __name__ == "__main__":
    process = multiprocessing.Process(target=WSC_main)
    process.start()
    main()

