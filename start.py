import time, json
import Motor.stepmoter_set as step
from HX711py.RoadCellOutput import Massdetection
import LCD.LCD_Output as lcd
from WSC.feedupdate import load_pet_info
from WSC.RaspberyTotal import WSC_main
import multiprocessing
from collections import OrderedDict

file_data = OrderedDict()
feedmass = Massdetection()
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

def default_set(times, sec):
    global avg
    i = 0
    set_list = []
    numdict = {1:'1st', 2:'2nd', 3:'3rd', 4:'4th', 5:'5th', 6:'6th'}
    while i < times:
        i += 1
        print(f"Output {numdict[i]}..")
        lcd.lcd_string(f"Output {numdict[i]}..", LCD_LINE_1)
        lcd.lcd_string(f"Woking {sec}Sec..", LCD_LINE_2)
        step.StepmoterRun(sec)
        time.sleep(2)

        weight = feedmass.weight_input()
        if i > 1 :
            weight = weight-sum(set_list[:i-1])
        lcd.lcd_string(f"Input {weight}g", LCD_LINE_2)
        set_list.append(weight)
        time.sleep(3)
    
    avg = sum(set_list)/len(set_list)
    print(set_list)
    lcd.lcd_string("Setup is Done", LCD_LINE_1)
    lcd.lcd_string(f'average:{avg}g', LCD_LINE_2)
    time.sleep(5)

    file_data["Avg"] = avg
    with open('Feeder_set.json', 'w', encoding="utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii=False)
    return avg

def feed_output(amount, avg):
    work_time = round(amount / avg)
    lcd.lcd_string(f"{work_time}Sec run for", LCD_LINE_1)
    lcd.lcd_string(f"{amount}g output", LCD_LINE_2)
    time.sleep(3)
    lcd.lcd_string("Doing output..", LCD_LINE_1)
    lcd.lcd_string(f"{work_time}Sec will work", LCD_LINE_2)

    step.StepmoterRun(work_time)
    lcd.lcd_string("Done output", LCD_LINE_1)
    lcd.lcd_string(f"{amount}g outputed", LCD_LINE_2)
    time.sleep(5)
    
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

        CrtTime = time.strftime('%H:%M:%S')
        
        # 현재 시각과 지정된 시간 대조 조건문 
        pet_data_list = [pet_data['pet_feed_time_B'], pet_data['pet_feed_time_L'], pet_data['pet_feed_time_D']]
        if avg and CrtTime in pet_data_list:
            feed_output(amount, avg)
        else:
            lcd.lcd_string("Current Time", LCD_LINE_1)
            lcd.lcd_string(CrtTime, LCD_LINE_2)

        # Refresh 빈도 설정
        time.sleep(0.5)

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
    


        