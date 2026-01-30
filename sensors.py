import smbus2
import time

# Registers
HUM_LSB = 0xFE
HUM_MSB = 0xFD
TEMP_XLSB = 0xFC
TEMP_LSB = 0xFB
TEMP_MSB = 0xFA
PRESS_XLSB = 0xF9
PRESS_LSB = 0xF8
PRESS_MSB = 0xF7
CONFIG = 0xF5
CTRL_MEAS = 0xF4
STATUS = 0xF3
RESET = 0xE0
ID = 0xD0

class bme280:
    def __init__(self, adress, bus):
        self.adress = adress
        self.bus = smbus2.SMBus(bus)
        self.__setup()
        self.calib = self.__get_calibration()
    
    def __setup(self):
        self.bus.write_byte_data(self.adress, CTRL_MEAS, 0x27)
        self.bus.write_byte_data(self.adress, 0xF2, 0x01)
        self.bus.write_byte_data(self.adress, 0xF5, 0xA0)
        time.sleep(0.1)

    def __read_ubyte(self, register):
        data = self.bus.read_i2c_block_data(self.adress, register, 2)
        data = (data[1] << 8) | data[0]
        return data

    def __read_sbyte(self, register):
        data = self.__read_ubyte(register)
        if data > 32767:
            data -= 65536
        return data
    
    def __get_calibration(self):
        calib = {}
        calib['dig_T1'] = self.__read_ubyte(0x88)
        calib['dig_T2'] = self.__read_sbyte(0x88 + 2)
        calib['dig_T3'] = self.__read_sbyte(0x88 + 4)
        calib['dig_P1'] = self.__read_ubyte(0x88 + 6)
        calib['dig_P2'] = self.__read_sbyte(0x88 + 8)
        calib['dig_P3'] = self.__read_sbyte(0x88 + 10)
        calib['dig_P4'] = self.__read_sbyte(0x88 + 12)
        calib['dig_P5'] = self.__read_sbyte(0x88 + 14)
        calib['dig_P6'] = self.__read_sbyte(0x88 + 16)
        calib['dig_P7'] = self.__read_sbyte(0x88 + 18)
        calib['dig_P8'] = self.__read_sbyte(0x88 + 20)
        calib['dig_P9'] = self.__read_sbyte(0x88 + 22)
        calib_H = [self.bus.read_byte_data(self.adress, 0xE1 + i) for i in range(0, 7)]
        calib_H.append(self.bus.read_byte_data(self.adress, 0xA1))
        calib['dig_H2'] = (calib_H[1]) << 8 | calib_H[0]
        calib['dig_H3'] = calib_H[2]
        calib['dig_H4'] = (calib_H[3] << 4) | (0x0F & calib_H[4])
        calib['dig_H5'] = (calib_H[5] << 4) | ((calib_H[4] >> 4) & 0x0F)
        calib['dig_H6'] = calib_H[6]
        calib['dig_H1'] = calib_H[7]

        for i in range(2, 7):
            if calib[f'dig_H{i}'] & 0x8000:
                calib[f'dig_H{i}'] = (-calib[f'dig_H{i}'] ^ 0xFFFF) + 1
            else: pass

        return calib

    def __read_rawtemp(self):
        data = self.bus.read_i2c_block_data(self.adress, TEMP_MSB, 3)
        data = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        return data

    def __read_rawpress(self):
        data = self.bus.read_i2c_block_data(self.adress, PRESS_MSB, 3)
        data = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        return data

    def __read_rawhum(self):
        data = self.bus.read_i2c_block_data(self.adress, HUM_MSB, 2)
        data = (data[0] << 8) | data[1]
        return data

    def get_temp(self):
        rawtemp = self.__read_rawtemp()
        var1 = ((((rawtemp >> 3) - (self.calib['dig_T1'] << 1))) * self.calib['dig_T2']) >> 11
        var2 = (((((rawtemp >> 4) - self.calib['dig_T1']) * ((rawtemp >> 4) - self.calib['dig_T1'])) >> 12) * self.calib['dig_T3']) >> 14
        t_raw = var1 + var2
        temp = ((t_raw * 5 + 128) >> 8) / 100
        self.t = t_raw
        return temp

    def get_press(self):
        rawpress = self.__read_rawpress()
        rawtemp = self.get_temp()
        var1 = self.t - 128000
        var2 = var1**2 * self.calib['dig_P6']
        var2 = var2 + ((var1 * self.calib['dig_P5']) << 17)
        var2 = var2 + ((self.calib['dig_P4']) << 35)
        var1 = ((var1 * var1 * self.calib['dig_P3']) >> 8) + ((var1 * self.calib['dig_P2']) << 12)
        var1 = (((1 << 47) + var1)) * (self.calib['dig_P1']) >> 33
        if var1 == 0: return 0
        else: pass
        p = 1048576 - rawpress
        p = (((p << 31) - var2) * 3125) / var1
        p = int(p)
        var1 = ((self.calib['dig_P9']) * (p >> 13) * (p >> 13)) >> 25
        var2 = ((self.calib['dig_P8']) * p) >> 19
        p = ((p + var1 + var2) >> 8) + ((self.calib['dig_P7']) << 4)
        p = p / 256 / 100
        return p

    def get_hum(self):
        rawhum = self.__read_rawhum()
        rawtemp = self.get_temp()
        
        v_x1_u32r = self.t - 76800
 
        v_x1_u32r = ((((rawhum << 14) - ((int(self.calib['dig_H4']) << 20) - (int(self.calib['dig_H5']) * v_x1_u32r)) + (16384)) >> 15) * (((((((v_x1_u32r * int(self.calib['dig_H6'])) >> 10) * (((v_x1_u32r * int(self.calib['dig_H3'])) >> 11) + (32768))) >> 10) + (2097152)) * int(self.calib['dig_H2']) + 8192) >> 14))
        v_x1_u32r = (v_x1_u32r - (((((v_x1_u32r >> 15) * (v_x1_u32r >> 15)) >> 7) * int(self.calib['dig_H1'])) >> 4))
        v_x1_u32r = 0 if v_x1_u32r < 0 else v_x1_u32r
        v_x1_u32r = 419430400 if v_x1_u32r > 419430400 else v_x1_u32r
        v_x1_u32r = v_x1_u32r >> 12
        v_x1_u32r = v_x1_u32r / 1024
        return v_x1_u32r

class bmp280:
    def __init__(self, adress, bus):
        self.adress = adress
        self.bus = smbus2.SMBus(bus)
        self.__setup()
        self.calib = self.__get_calibration()
    
    def __setup(self):
        self.bus.write_byte_data(self.adress, CTRL_MEAS, 0x27)
        self.bus.write_byte_data(self.adress, 0xF5, 0xA0)

    def __read_ubyte(self, register):
        data = self.bus.read_i2c_block_data(self.adress, register, 2)
        data = (data[1] << 8) | data[0]
        return data

    def __read_sbyte(self, register):
        data = self.__read_ubyte(register)
        if data > 32767:
            data -= 65536
        return data
    
    def __get_calibration(self):
        calib = {}
        calib['dig_T1'] = self.__read_ubyte(0x88)
        calib['dig_T2'] = self.__read_sbyte(0x88 + 2)
        calib['dig_T3'] = self.__read_sbyte(0x88 + 4)
        calib['dig_P1'] = self.__read_ubyte(0x8E)
        calib['dig_P2'] = self.__read_sbyte(0x8E + 2)
        calib['dig_P3'] = self.__read_sbyte(0x8E + 4)
        calib['dig_P4'] = self.__read_sbyte(0x8E + 6)
        calib['dig_P5'] = self.__read_sbyte(0x8E + 8)
        calib['dig_P6'] = self.__read_sbyte(0x8E + 10)
        calib['dig_P7'] = self.__read_sbyte(0x8E + 12)
        calib['dig_P8'] = self.__read_sbyte(0x8E + 14)
        calib['dig_P9'] = self.__read_sbyte(0x8E + 16)
        return calib

    def __read_rawtemp(self):
        data = self.bus.read_i2c_block_data(self.adress, TEMP_MSB, 3)
        data = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        return data

    def __read_rawpress(self):
        data = self.bus.read_i2c_block_data(self.adress, PRESS_MSB, 3)
        data = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        return data

    def get_temp(self):
        rawtemp = self.__read_rawtemp()
        var1 = ((((rawtemp >> 3) - (self.calib['dig_T1'] << 1))) * self.calib['dig_T2']) >> 11
        var2 = (((((rawtemp >> 4) - self.calib['dig_T1']) * ((rawtemp >> 4) - self.calib['dig_T1'])) >> 12) * self.calib['dig_T3']) >> 14
        t_raw = var1 + var2
        temp = ((t_raw * 5 + 128) >> 8) / 100
        self.t = t_raw
        return temp

    def get_press(self):
        rawpress = self.__read_rawpress()
        var1 = self.t - 128000
        var2 = var1**2 * self.calib['dig_P6']
        var2 = var2 + ((var1 * self.calib['dig_P5']) << 17)
        var2 = var2 + ((self.calib['dig_P4']) << 35)
        var1 = ((var1 * var1 * self.calib['dig_P3']) >> 8) + ((var1 * self.calib['dig_P2']) << 12)
        var1 = (((1 << 47) + var1)) * (self.calib['dig_P1']) >> 33
        if var1 == 0: return 0
        else: pass
        p = 1048576 - rawpress
        p = (((p << 31) - var2) * 3125) / var1
        p = int(p)
        var1 = ((self.calib['dig_P9']) * (p >> 13) * (p >> 13)) >> 25
        var2 = ((self.calib['dig_P8']) * p) >> 19
        p = ((p + var1 + var2) >> 8) + ((self.calib['dig_P7']) << 4)
        p = p / 256 / 100
        return p