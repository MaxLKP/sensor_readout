from bmp280_i2c import *

bmp280 = bmp280(0x76, 1)
bmp280.setup()
rawtemp = bmp280.read_rawtemp()
rawpress = bmp280.read_rawpress()
calib = bmp280.get_calibration()
temp, t = bmp280.get_temp(rawtemp, calib)
press = bmp280.get_press(rawpress, calib, t)

print(temp)
print(press)