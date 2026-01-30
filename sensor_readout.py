from influxdb import InfluxDBClient
from sensors import *

bme280 = bme280(0x76, 1)

#client = InfluxDBClient(host = 'localhost', port = 8086, dbname = 'db')
client = InfluxDBClient(host = 'localhost', port = 8086)
client.switch_database('db')

temp = bme280.get_temp()
press = bme280.get_press()
hum = bme280.get_hum()

client.write_points([{"measurement": "bme280", "tags": {"location": "blueberry"}, "fields": {"value": temp}}])
client.write_points([{"measurement": "bme280", "tags": {"location": "blueberry"}, "fields": {"value": press}}])
client.write_points([{"measurement": "bme280", "tags": {"location": "blueberry"}, "fields": {"value": hum}}])
client.close()
