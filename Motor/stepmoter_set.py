import RPi.GPIO as g
import time

def StepmoterRun(settime):
    g.setwarnings(False)
    g.setmode(g.BCM)
    StepPins = [17,27,22,23] # Stepmoter set pin
    for pin in StepPins:
        g.setup(pin, g.OUT)
        g.output(pin, False)

    dd = 0
    StepCounter = 0
    StepCount = 4
    count = 0
    Seq = [
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1]]

    begin = time.time()
    while True:
        end = time.time()
        result = end-begin
        if result <= settime :
            tt = int(result)+1
            if tt != dd:
                print(tt)
                # LCD 출력
                # lcd.lcd_string(f"{tt}Sec..", 0xC0)
                dd += 1
            for pin in range(0,4):
                xpin = StepPins[pin]
                if Seq[StepCounter][pin] != 0 :
                    g.output(xpin, True)
                else:
                    g.output(xpin, False)

            StepCounter += 1
            count += 1
            if(StepCounter == StepCount):
                StepCounter = 0
            if (StepCounter <0):
                StepCounter = StepCount

            time.sleep(0.002)
        else:
            for i in StepPins:
                g.output(i, False)
            print(count/4)
            break

def StepmoterRun2(settime):
    g.setwarnings(False)
    g.setmode(g.BCM)
    StepPins = [17,27,22,23] # Stepmoter set pin
    for pin in StepPins:
        g.setup(pin, g.OUT)
        g.output(pin, False)

    StepCounter = 0
    StepCount = 4
    count = 0
    Seq = [
        [1,1,0,0],
        [0,1,1,0],
        [0,0,1,1],
        [1,0,0,1],
    ]

    while True:
        angle = settime*512/90
        if count < angle :
            for pin in range(0,4):
                xpin = StepPins[pin]
                if Seq[StepCounter][pin] != 0 :
                    g.output(xpin, True)
                else:
                    g.output(xpin, False)

            StepCounter += 1
            count += 1
            if(StepCounter == StepCount):
                StepCounter = 0
            if (StepCounter <0):
                StepCounter = StepCount





            time.sleep(0.0015)
        else:
            for i in StepPins:
                g.output(i, False)
            print(f'{int(count/512*90)}도 회전')
            break

if  __name__ == "__main__":
    StepmoterRun2(1440)
