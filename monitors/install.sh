#!/bin/bash

# Script takes arguments: server 
# Example: ./install.sh -s dennis@localhost 
while getopts s:p: flag
do
    case "${flag}" in
        s) server=${OPTARG};;
    esac
done

# Installs git:
sudo apt-get install git

# Update the system and upgrade the packages
apt-get update
# apt-get upgrade -y
echo "System updated"

# Install perf on the system (for performance monitoring)
apt install linux-perf -y
echo "perf was installed"

# Copies the files m1.service and m2.service and m3.service to /etc/systemd/system/:
cd services 
cp m1.service m2.service m3.service m3.env /etc/systemd/system/
systemctl daemon-reload
echo "Services copied to /etc/systemd/system/"
echo "Services reloaded"

# Creates the .env file for the 3rd monitor:
apt install python3-venv -y
cd ..
cd monitor1
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
deactivate
echo "Virtual environment created and requirements installed"

# Make monitor2 and monitor3 executable:
cd ..
cd monitor2
chmod +x new_sampler_50tmp.sh

cd ..
cd monitor3
chmod +x monitor.sh

echo "Monitor2 and monitor3 made executable"




