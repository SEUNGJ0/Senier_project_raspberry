import RPi.GPIO as g
import time

def StepmoterRun(settime):
    g.setwarnings(False)
    g.setmode(g.BCM)

    step_sequence = [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1],
    ]


    # Set up motor pins
    step_pins = [17, 27, 22, 23]
    for pin in step_pins:

        g.setup(pin, g.OUT)
        g.output(pin, False)

    # Initialize variables
    step_count = len(step_sequence)
    step_counter = 0
    count = 0

    # 모터 작동 및 스텝 카운트
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > settime:
            break

        # 모터 핀 업데이트
        for pin in range(len(step_pins)):
            xpin = step_pins[pin]
            if step_sequence[step_counter][pin] == 1:
                g.output(xpin, True)
            else:
                g.output(xpin, False)

        # step counter 업데이트
        step_counter += 1
        if step_counter == step_count:
            step_counter = 0
        count += 1

        # 모터 속도 조절
        time.sleep(0.002)

    # 모터 정지 및 count 출력
    for pin in step_pins:
        g.output(pin, False)
    print(count)



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





            time.sleep(0.002)
        else:
            for i in StepPins:
                g.output(i, False)
            print(f'{int(count/512*90)}도 회전')
            break

if  __name__ == "__main__":
    # StepmoterRun2(1440)
    StepmoterRun(30)
