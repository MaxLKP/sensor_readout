# Sensor Readout
Readout of sensors connected to *Raspberry Pi 0 w2*. 
## I2C Readout
For the BMP280, BME280 and ADS1115 readout scripts provide basic functionality to read the sensors using the I2C interface. 
## Readout
The sensor readout reads the desired sensors and writes them to an influxdb instance. The readout configuration (database name, readout frequency, etc.) can be set using config.yaml.