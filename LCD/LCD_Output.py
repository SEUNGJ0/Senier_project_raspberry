import smbus
import time

# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
    # LCD 초기화
    lcd_byte(0x33,LCD_CMD) # 110011 Initialise
    lcd_byte(0x32,LCD_CMD) # 110010 Initialise
    lcd_byte(0x06,LCD_CMD) # 000110 커서 이동 방향
    lcd_byte(0x0C,LCD_CMD) # 001100 화면 켜기, 커서 끄기, 깜빡임 끄기
    lcd_byte(0x28,LCD_CMD) # 101000 데이터 길이, 라인 수, 폰트 크기
    lcd_byte(0x01,LCD_CMD) # 000001 디스플레이 지우기
    time.sleep(E_DELAY)

def lcd_toggle_enable(bits):
    # enable 핀을 1로 설정하고, 0으로 설정하여 enable 신호를 토글링
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
    time.sleep(E_DELAY)
    
def lcd_byte(bits, mode):
    # 데이터를 LCD에 전송하기 위해 데이터 핀과 enable 핀 설정
    # mode가 1이면 데이터, 0이면 명령어
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

    # 상위 비트 전송
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # 하위 비트 전송
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_string(message,line):
    # 문자열을 해당 라인에 출력
    message = message.ljust(LCD_WIDTH," ")
    line_index = {1:0x80, 2:0xC0}
    lcd_byte(line_index[line], LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)


def lcd_integer(intdata, line):
    lcd_byte(line, LCD_CMD)
    lcd_byte(intdata, LCD_CHR)

def main():
	# Main program block

	# Initialise display
	lcd_init()

	while True:
    # Send some test
    lcd_string("TESTWORD       <",LCD_LINE_1)
    lcd_string("I2C LCD        <",LCD_LINE_2)

    time.sleep(1)

    # Send some more text
    lcd_string(">         RPiSpy",LCD_LINE_1)
    lcd_string(">        I2C LCD",LCD_LINE_2)

    time.sleep(1)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass
	finally:
		lcd_byte(0x01, LCD_CMD)