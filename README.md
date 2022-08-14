# Monitor Controller Repository File structure:
* `/monitors`: contains the monitoring scripts (RES, KERN and SYS)
* `/helpers`: contain the randomfile generator and ressource monitor (CPU & Memory measuring script) with instructions
* `/middleware`: contains the actual middleware and controlls the monitoring scripts (KERN, RES and SYS)
* `install_source.sh`: To install all needed dependencies for the Monitor Controller

This Repository is part of the thesis: 
Intelligent Framework to Detect Ransomware Affecting Linux-based and Resource-constrained Devices
The repository for the Flas Data Analysis Application can be found here: https://github.com/dennisshushack/BA_Thesis_Flask

If you have any troubles installing the Monitor Controller or other parts of the system feel free to contact me: dennis.shushack@uzh.ch


It is **highly** suggested to have a Linux or BSD based operating system running on your main machine. Mac OS should also work fine.
Windows on the other hand can be troublesome. If you run a Windows distribution, please consider dualbooting or installing a distro on an external SSD i.e. Ubuntu. It is also recommendet to have your machine connected via LAN and not WIFI, due to Network drops.

Furthermore, the Monitor Controller saves all data in the `/tmp` folder on the Raspberry PI (/tmp/todo.db is the database /tmp/monitors is the folder where all data is saved temporerly on the PI.)

# Monitor Controller Instalation:

## Prerequisite:
You should have an ElectroSense sensor deployed and can SSH into it. 
You have a Linux/BSD based operating system running on your machine.

### Enabling SSH on Desktop/Server
You will need to enable SSH on your main machine. That way the sensor can rsync the data monitored to your device. Depending on the choosen operating system this step may vary. Assuming a Debian-based OS i.e. Ubuntu execute the following commands:
```
sudo apt-get install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
```

To check if the openssh-server is running use the following command:
```
sudo systemctl status ssh
```
You should now be able to SSH into your machine usining `ssh yourusername@PCIpAddress`. You can get your ip using the following instructions:
```
sudo apt-get install net-tools
ifconfig
```
You can test if you can SSH from the Raspberry PI onto your main computer. 

## Installation of the Monitor Controller on the Raspberry PI:
The installation is fairly simple, please just follow the folling commands:
You will get prompted to insert your password (for the computer)
This installs all dependencies needed.

```
# Update the packages on the sensor:
apt-get update

# Install Git:
apt-get git

# Clone the repository:
git clone https://github.com/dennisshushack/BA_Thesis_PI.git

# Change Directory into the Git Repo:
cd BA_Thesis_PI

# Give access to the installer script:
chmod +x install_source.sh

# Run installer script (User will be prompted to enter his password)
./install_source.sh -s username@serveripaddress
```






