import RPi.GPIO as GPIO
import time

class StepperMotor:
    def __init__(self, pins=[17, 27, 22, 23]):
        self.pins = pins
        self.sequence = [
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1],
            [1, 0, 0, 1],
        ]
        self.step_count = len(self.sequence)
        self.step_counter = 0
        self.count = 0

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def run_with_time(self, settime):
        start_time = time.time()

        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > settime:
                break

            for pin in range(len(self.pins)):
                xpin = self.pins[pin]
                if self.sequence[self.step_counter][pin] == 1:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)

            self.step_counter += 1
            if self.step_counter == self.step_count:
                self.step_counter = 0
            self.count += 1

            time.sleep(0.002)

        for pin in self.pins:
            GPIO.output(pin, False)
            
    def run_with_angle(self, setangle):
        StepCount = 4
        count = 0
        angle = setangle * 512 / 90

        while count < angle:
            for pin in range(0, 4):
                xpin = self.pins[pin]
                if self.sequence[self.step_counter][pin] == 1:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)

            self.step_counter += 1
            count += 1
            if self.step_counter == StepCount:
                self.step_counter = 0
            if self.step_counter < 0:
                self.step_counter = StepCount

            time.sleep(0.002)

        for i in self.pins:
            GPIO.output(i, False)
        print(f'{int(count/512*90)}도 회전')
    
    def run_with_command(self, stop_event):
        while not stop_event.is_set():
            for pin in range(len(self.pins)):
                xpin = self.pins[pin]
                if self.sequence[self.step_counter][pin] == 1:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)
            time.sleep(0.002)
            self.step_counter += 1
            if self.step_counter == self.step_count:
                self.step_counter = 0
            self.count += 1
        
        print("모터 작동 종료")
        for pin in self.pins:
            GPIO.output(pin, False)
    
if __name__ == "__main__":
    Moter_1 = StepperMotor()
    print("모터 작동 시작")
    for i in range(10000):
        Moter_1.run_with_command()
        time.sleep(0.002)
