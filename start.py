import time
import Motor.stepmoter_set as step
from hx711py.example import weight_input
import LCD.LCD_Output as lcd

import schedule
import json
from collections import OrderedDict

file_data = OrderedDict()

def defaul_set(times, sec):
    global avg
    i = 0
    set_list = []
    numdict = {1:'1st', 2:'2nd', 3:'3rd', 4:'4th', 5:'5th', 6:'6th'}
    while i < times:
        i += 1
        print(f"Output {numdict[i]}..")
        lcd.lcd_string(f"Output {numdict[i]}..", 0x80)
        lcd.lcd_string(f"Woking {sec}Sec..", 0xC0)
        step.StepmoterRun(sec)
        time.sleep(2)

        weight = weight_input()
        lcd.lcd_string(f"Input {weight}g", 0xC0)
        set_list.append(weight)
        time.sleep(3)
    
    avg = sum(set_list)/len(set_list)
    print(set_list)
    lcd.lcd_string("Setup is Done", 0x80)
    lcd.lcd_string(f'average:{avg}g', 0xC0)
    time.sleep(5)

    file_data["Avg"] = avg
    with open('Pet_Data.json', 'w', encoding="utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii=False)

def feed_output(amount):
    work_time = round(amount / avg)
    lcd.lcd_string(f"{work_time}Sec run for", 0x80)
    lcd.lcd_string(f"{amount}g output", 0xC0)
    time.sleep(3)
    lcd.lcd_string("Doing output..", 0x80)
    lcd.lcd_string(f"{work_time}Sec will work", 0xC0)

    step.StepmoterRun(work_time)
    lcd.lcd_string("Done output", 0x80)
    lcd.lcd_string(f"{amount}g outputed", 0xC0)
    time.sleep(5)


def time_set_output(set_time, amount):
    schedule.every().day.at(set_time).do(feed_output, amount)
    while True:
        if set_time == time.strftime('%H:%M'):
            schedule.run_pending()
            break
        else:
            lcd.lcd_string("Current Time", 0x80)
            lcd.lcd_string(time.strftime('%H:%M:%S'), 0xC0)
            continue
    

try:
    with open('Pet_Data.json', 'r') as f:
        Pet_Json = json.load(f)
    avg = Pet_Json['Avg']  

except:
    avg = None

while True:
    # LCD 초기화
    lcd.lcd_init()
    if avg:
        time_set_output('15:17', 300)
    else:
        lcd.lcd_string("Error!!", 0x80)
        lcd.lcd_string('Avg not set!', 0xC0)
        time.sleep(5)
        lcd.lcd_string('Start setup....', 0xC0)
        time.sleep(3)
        defaul_set(5, 5)

        
