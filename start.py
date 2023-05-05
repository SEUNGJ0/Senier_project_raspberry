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
    i = 0
    is_running = True
    def run_motor():
        while is_running:
            STM.run_with_command(is_running)
            time.sleep(0.002)
        STM.run_with_command(is_running)
    t = threading.Thread(target=run_motor)
    t.start()
    while(True):
        lcd.lcd_string(f"Measured : {feedmass.weight_input()}g", LCD_LINE_2)
        time.sleep(0.1)
        if feedmass.weight_input() >= amount:
            is_running = False
            t.join()
            print(feedmass.weight_input())
            return feedmass.weight_input()

def main():
    # LCD 초기화
    lcd.lcd_init()
    while True:
        # 사용자가 설정한 펫 정보데이터와 하루 지급 사료량 읽어옴
        amount, pet_data = load_pet_info()

        CrtTime = time.strftime('%H:%M')
        
        # 현재 시각과 지정된 시간 대조 조건문 
        pet_data_list = [pet_data['pet_feed_time_B'], pet_data['pet_feed_time_L'], pet_data['pet_feed_time_D']]
        epf_args_list = [0, 0, 0, 0, 0, 0]
        today_feed, feed_data = read_today_data()
        if CrtTime in pet_data_list:
            feed_index = int(pet_data_list.index(CrtTime))
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
