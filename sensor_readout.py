from influxdb import InfluxDBClient
from sensors import *
import time

bme280 = bme280(0x76, 1)

#client = InfluxDBClient(host = 'localhost', port = 8086, dbname = 'db')
client = InfluxDBClient(host = 'localhost', port = 8086)
client.switch_database('db')

while True:
    temp = round(bme280.get_temp(), 2)
    press = round(bme280.get_press(), 2)
    hum = round(bme280.get_hum(), 2)
    print(f"Wrote to DB: {temp}, {press}, {hum}")
    client.write_points([{"measurement": "bme280_temp", "tags": {"location": "blueberry"}, "fields": {"value": temp}}])
    client.write_points([{"measurement": "bme280_press", "tags": {"location": "blueberry"}, "fields": {"value": press}}])
    client.write_points([{"measurement": "bme280_hum", "tags": {"location": "blueberry"}, "fields": {"value": hum}}])
    time.sleep(5)
client.close()
