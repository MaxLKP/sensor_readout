# Sensor Readout
Readout of sensors using [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/). 
## I2C Readout
For the [BMP280](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp280-ds001.pdf), [BME280](https://www.bosch-sensortec.com/products/environmental-sensors/humidity-sensors-bme280/) and [ADS1115](https://www.ti.com/product/ADS1115) readout scripts provide basic functionality to read the sensors using the [I2C](https://en.wikipedia.org/wiki/I2C) interface. The utilities are used for the readout. 
## Readout
The sensor readout reads the desired sensors and writes them to an [InfluxDB](https://www.influxdata.com/) instance. The readout configuration (database name, readout frequency, etc.) can be set using config.yaml. The data can be visulized using [Grafana](https://grafana.com/).
## Setup
To facilitate the setup, setup.sh can be run. This installs all dependencies, creates a directory in ~/home/user/sensors_readout with the GIT repository, and starts InfluxDB and Grafana. The standard database created and used is named "db". The I2C interface of the Raspberry has to be enabled.

Furthermore, the following python packages might need to be installed (e.g. via pip):
- [smbus2](https://pypi.org/project/smbus2/)
- [influxdb](https://pypi.org/project/influxdb/)

The script setup.sh should take care of installing everything else, but is yet to be tested on a fresh OS.