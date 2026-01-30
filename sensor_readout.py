from influxdb import InfluxDBClient
from sensors import *
import time
import yaml

config_file = "/home/blueberry/sensors/config.yaml"

with open (config_file , 'r') as file:
    config = yaml.safe_load(file)

db = config["database"]["name"]
frequency = int(config["readout"]["delay"])
output = config["readout"]["output"]

bme280 = bme280(0x76, 1)

client = InfluxDBClient(host = 'localhost', port = 8086)
client.switch_database(db)

try:
    while True:
        temp = round(bme280.get_temp(), 2)
        press = round(bme280.get_press(), 2)
        hum = round(bme280.get_hum(), 2)
        if output == True:
            print(f"Wrote to DB: {temp}, {press}, {hum}")
        else: pass
        client.write_points([{"measurement": "bme280_temp", "tags": {"location": "blueberry"}, "fields": {"value": temp}}])
        client.write_points([{"measurement": "bme280_press", "tags": {"location": "blueberry"}, "fields": {"value": press}}])
        client.write_points([{"measurement": "bme280_hum", "tags": {"location": "blueberry"}, "fields": {"value": hum}}])
        time.sleep(frequency)
except KeyboardInterrupt:
    client.close()
    print("Terminated Sensor Readout. Client closed.")
