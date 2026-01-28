from ads1115_i2c import *
import time

ads1115 = ads1115(0x48, 1)

while True:
    data = ads1115.read_value()
    print(data)
    time.sleep(2)

