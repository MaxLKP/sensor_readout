#!/bin/bash
# Prepare Folder
export PATH="/bin:/usr/bin:/usr/local/bin:$PATH"
USER="$(logname)"
PATH="/home/${USER}/sensors_readout"
echo "Creating Path for readout: ${PATH}"
/bin/mkdir /home/${USER}/sensors_readout
cd ${PATH}
#Prepare InfluxDB
printf "${Green}Installing InfluxDB\n"
/bin/curl https://repos.influxdata.com/influxdata-archive.key | /bin/gpg --dearmor | /bin/sudo tee /usr/share/keyrings/influxdb-archive-keyring.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/influxdb-archive-keyring.gpg] https://repos.influxdata.com/debian stable main" | sudo tee /etc/apt/sources.list.d/influxdb.list
/bin/deb [signed-by=/usr/share/keyrings/influxdb-archive-keyring.gpg] https://repos.influxdata.com/debian stable main
/bin/sudo apt update
/bin/sudo apt install influxdb
printf "${Green}Staring Influx service\n"
/bin/sudo systemctl unmask influxdb
/bin/sudo systemctl enable influxdb
/bin/sudo systemctl start influxdb
printf "${Green}Creating Database\n"
/bin/influx -execute "CREATE DATABASE db"
#Get Sensor Readout
printf "${Green}Get Sensor Readout from GIT\n"
/bin/sudo apt-get install git
/bin/git init
/bin/git pull https://github.com/MaxLKP/sensor_readout.git
#Prepare Grafana
printf "${Green}Install Grafana\n"
/bin/sudo mkdir -p /etc/apt/keyrings/
/bin/wget -q -O - https://apt.grafana.com/gpg.key | /bin/gpg --dearmor | /bin/sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | /bin/sudo tee /etc/apt/sources.list.d/grafana.list
/bin/deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main
/bin/sudo apt-get update
printf "${Green}Start Grafana Service\n"
/bin/sudo /bin/systemctl enable grafana-server
/bin/sudo /bin/systemctl start grafana-server