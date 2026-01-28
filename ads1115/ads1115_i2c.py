import smbus2
import time

class ads1115():
    def __init__(self, adress, bus):
        self.adress = adress
        self.bus = smbus2.SMBus(bus)
        #self.__set_config()

    def __set_config(self):
        self.bus.write_i2c_block_data(self.adress, 0x01, [0x84, 0x83])
        time.sleep(0.1)

    def __read_register(self):
        self.bus.write_i2c_block_data(self.adress, 0x01, [0x84, 0x83])
        self.bus.write_byte(self.adress, 0x00)
        time.sleep(0.1)
        data = self.bus.read_i2c_block_data(self.adress, 0x00, 2)
        data = (data[0] << 8) | data[1]
        if data > 32787:
            data = data - 65536
        else: pass
        return data

    def read_value(self):
        data = self.__read_register()
        value = 4.096 / data
        #value = data
        return value



    