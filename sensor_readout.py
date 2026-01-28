from influxdb import InfluxDBClient
from sensors import *

bme280 = bme280(0x76, 1)

#client = InfluxDBClient(host = 'localhost', port = 8086, dbname = 'db')
client = InfluxDBClient(host = 'localhost', port = 8086)
client.switch_database('db')

temperature = bme280.get_temp()

client.write_points([{"measurement": "bme280_temp", "tags": {"location": "blueberry"}, "fields": {"value": temperature}}])
client.close()
