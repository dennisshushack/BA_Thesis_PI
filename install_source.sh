#!/bin/bash

###############################################################################
# Script takes arguments: server -s
# Example: ./install.sh -s dennis@localhost
# Will install everything necessary for the monitors to run on the server
# and creates a passwordless ssh connection between the server and rasperry pi
###############################################################################

while getopts s:p: flag
do
    case "${flag}" in
        s) server=${OPTARG};;
    esac
done

# Create a passwordless ssh connection to a server:
# Check if id_rsa.pub already exists
mkdir ~/.ssh/
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
ssh-copy-id -i ~/.ssh/id_rsa.pub $server
echo "SSH connection created"

# Update the system and upgrade the packages
apt-get update
echo "System updated"

# Install perf on the system (for performance monitoring)
apt install linux-perf -y
echo "perf was installed"

# Installs python-venv
apt install python3-venv -y
echo "Installed python-venv"

# Install support for ExFat (SSD) can be ignored if not need:
apt install exfat-fuse exfat-utils -y

# Copies the files m1.service and m2.service and m3.service to /etc/systemd/system/:
cd monitors/services
cp m2.service m3.service m3.env /etc/systemd/system/
cp m1_source.service /etc/systemd/system/m1.service
systemctl daemon-reload
echo "Services copied to /etc/systemd/system/"
echo "Services reloaded"

# Creates the .env file for the 1st monitor and installs requirements.txt:
cd ..
cd monitor1/source
python3 -m venv env
source env/bin/activate
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
deactivate
echo "Virtual environment created and requirements installed for monitor 1"

# Make monitor2 and monitor3 executable:
cd ../../
cd monitor2
chmod +x new_sampler_50tmp.sh
cd ..
cd monitor3
chmod +x monitor.sh
echo "Monitor2 and monitor3 made executable"

# Installs the python-venv for the for the middleware:
cd ../../
cd middleware
python3 -m venv env
source env/bin/activate
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org tabulate requests click python-dotenv
deactivate
echo "Virtual environment created and requirements installed for middleware"








