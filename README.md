# Monitor Controller Repository File structure:
* `/monitors`: contains the monitoring scripts (RES, KERN and SYS)
* `/helpers`: contain the randomfile generator and ressource monitor (CPU & Memory measuring script) with instructions
* `/middleware`: contains the actual middleware and controlls the monitoring scripts (KERN, RES and SYS)
* `install_source.sh`: To install all needed dependencies for the Monitor Controller
* 
This Repository is part of a Bachelor's Thesis. This README.md provides some additional help. The main installation steps are described in the installation instructions in the paper.

The Flask Data Analysis Application repository can be found here: https://github.com/dennisshushack/BA_Thesis_Flask.

If you have trouble installing the Monitor Controller or other parts of the system, feel free to contact me: dennis.shushack@uzh.ch.

It is **highly** suggested to have a Linux or BSD-based operating system running on your main machine. Mac OS should also work fine.
Windows, on the other hand, can be troublesome. If you run a Windows distribution, please consider dual-booting or installing a distribution on an external SSD, i.e., Ubuntu. It is recommended to have your machine connected via LAN and not WIFI, due to Network drops.

Note, the Monitor Controller saves all essential data in the `/tmp` folder on the Raspberry PI ( i.e. /tmp/todo.db is the database,  /tmp/monitors is the folder where all data is saved temporarily on the PI.)

# Monitor Controller Instalation:

## Prerequisite:
You should have an ElectroSense sensor deployed and can SSH into it. 
You have a Linux/BSD-based operating system running on your machine.

### Enabling SSH on Desktop/Server
You will need to enable SSH on your main machine. That way, the sensor can sync the data monitored to your device. Depending on the chosen operating system, this step may vary. Assuming a Debian-based OS i.e., Ubuntu execute the following commands:
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

## Installation of the Monitor Controller on the Raspberry PI:
The installation of the Monitor Controller is relatively simple. Only a small amount of commands is required:

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
Before launching the Monitor Controller, perform the following instructions on the Raspberry Pi sensor: 
```
cd BA_Thesis_PI/middleware
source env/bin/activate
``
## Commands:
Four commands are available to the User: Show, Collect, Send and Live.
The user will be prompted to input additional information, after activiating on of these commands.

### Command Collect
For collecting training/evaluation data:
```
python3 cli.py collect
```

### Command Show
For viewing all past monitoring sessions:
```
python3 cli.py show
``

### Command Send:
For sending the metadata to the Data Anaylsis Application to start training/evaluating data
```
python3 cli.py send
```

### Command Live:
Starts a live monitoring session for 60 minutes
```
python3 cli.py live
``
