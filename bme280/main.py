from bme280_i2c import *
import time

bme280 = bme280(0x76, 1)

while True:
    temp = bme280.get_temp()
    press = bme280.get_press()
    hum = bme280.get_hum()
    print(temp)
    print(press)
    print(hum)
    time.sleep(2)