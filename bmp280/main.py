from bmp280_i2c import *
import time

bmp280 = bmp280(0x76, 1)

while True:
    temp = bmp280.get_temp()
    press = bmp280.get_press()

    print(temp)
    print(press)

    time.sleep(2)