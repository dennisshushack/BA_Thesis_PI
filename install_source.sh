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

# Update the system:
apt-get upgrade -y
echo "upgraded"

# Install perf on the system (for performance monitoring)
apt install linux-perf -y
echo "perf was installed"

# Installs python-venv
apt install python3-venv -y
echo "Installed python-venv"

# Can be activated if needed (SSD):
# apt install exfat-fuse exfat-utils -y

cd monitors/services
cp RES.service KERN.service SYS.service SYS.env /etc/systemd/system/
systemctl daemon-reload
echo "Services copied to /etc/systemd/system/"
echo "Services reloaded"

# RES Monitor
echo "Installing dependencies for the RES Monitor"
cd ..
cd RES/source
python3 -m venv env
source env/bin/activate
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
deactivate
echo "Depencencies installed"

# KERN Monitor and SYS Monitor
echo "Installing dependencies for the KERN and SYS Monitor"
cd ../../
cd KERN
chmod +x KERN.sh
cd ..
cd SYS
chmod +x SYS.sh
echo "Depencencies installed"

# Installs the python-venv for the for the middleware:
echo "Installing the dependencies for the Monitor Controller Middleware"
cd ../../
cd middleware
python3 -m venv env
source env/bin/activate
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org tabulate requests click python-dotenv
deactivate
echo "Depencencies installed"
echo "Done, you can start Monitoring"








