import time, json, multiprocessing
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

def default_set(times, work_time):
    global avg
    feedmass = Massdetection()
    lcd.lcd_init()
    i = 0
    numdict = {1:'1st', 2:'2nd', 3:'3rd', 4:'4th', 5:'5th', 6:'6th'}
    while i < times:
        i += 1
        print(f"Output {numdict[i]}..")
        lcd.lcd_string(f"Output {numdict[i]}..", LCD_LINE_1)
        lcd.lcd_string(f"Woking {work_time}Sec..", LCD_LINE_2)
        STM.run_with_time(work_time)
        time.sleep(2)
    
    weight = feedmass.weight_input()
    avg = (weight/times)/work_time
    lcd.lcd_string("Setup is Done", LCD_LINE_1)
    lcd.lcd_string(f'Avg Per Sec:{avg}g', LCD_LINE_2)
    time.sleep(4)

    file_data["Avg"] = avg
    with open('Feeder_set.json', 'w', encoding="utf-8") as make_file:
        json.dump(file_data, make_file)
    return avg

def feed_output(amount, avg):
    work_time = round(amount / avg)
    lcd.lcd_string(f"{work_time}Sec run for", LCD_LINE_1)
    lcd.lcd_string(f"{amount}g output", LCD_LINE_2)
    time.sleep(3)
    lcd.lcd_string("Doing output..", LCD_LINE_1)
    lcd.lcd_string(f"{work_time}Sec will work", LCD_LINE_2)

    STM.run_with_time(work_time)
    lcd.lcd_string("Done output", LCD_LINE_1)
    lcd.lcd_string(f"{amount}g outputed", LCD_LINE_2)
    time.sleep(3)
    
def main():
    try:
        with open('Feeder_set.json', 'r') as f:
            Pet_Json = json.load(f)
        avg = Pet_Json['Avg']
        print("avg : ",avg)
    except:
        avg = None

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
                feed_output(amount, avg)
                lcd.lcd_string("Done!!", LCD_LINE_1)
                lcd.lcd_string(f"Given: {amount}g", LCD_LINE_2)
                epf_args_list[feed_index+3] = amount
                edit_pet_feed(epf_args_list)
                time.sleep(5)

        else:
            lcd.lcd_string("Current Time", LCD_LINE_1)
            lcd.lcd_string(CrtTime, LCD_LINE_2)

        # Refresh 빈도 설정
        time.sleep(5)

        # 초당 사료 추출량의 평균 설정이 안되있는 경우 실행
        if not avg:
            lcd.lcd_string("Error!!", LCD_LINE_1)
            lcd.lcd_string('Avg not set!', LCD_LINE_2)
            time.sleep(3)
            lcd.lcd_string('Start setup....', LCD_LINE_2)
            time.sleep(3)
            # 추출 세팅 함수 실행 및 평균값 가져옴
            avg = default_set(5, 5)



if __name__ == "__main__":
    process = multiprocessing.Process(target=WSC_main)
    process.start()
    main()
    


        