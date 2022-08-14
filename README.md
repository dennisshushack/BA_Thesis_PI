# Monitor Controller Repository:

##  File structure 
* `/monitors`: Directory containing the monitoring scripts (RES, KERN and SYS).
* `/helpers`: Directory containing a random-file generator and ressource monitor (CPU & Memory utilization measuring script) with instructions.
* `/middleware`: Directory containing the Monitor Controller middleware, which controls the monitoring scripts (KERN, RES and SYS)
* `install_source.sh`: File to install all needed dependencies for the Monitor Controller

## Overview
This Repository is part of a Bachelor's Thesis. This README.md provides some additional help. The main installation steps are described in the installation instructions in the paper.

The Flask Data Analysis Application repository can be found here: https://github.com/dennisshushack/BA_Thesis_Flask.

If you have trouble installing the Monitor Controller or other parts of the system, feel free to contact me: dennis.shushack@uzh.ch.

It is **highly** recommended to have a Linux or BSD-based operating system running on your main machine. Mac OS should also work fine.
Windows, on the other hand, can be troublesome. If you are running Windows, please consider dual-booting or installing a different distribution i.e., Ubuntu. It is recommended to have your main machine connected via LAN and not WIFI, when using the Monitor Controller.

Note, the Monitor Controller saves all essential data in the `/tmp` folder on the Raspberry PI ( i.e. /tmp/todo.db is the database,  /tmp/monitors is the folder where all data is saved temporarily on the PI.). Be aware, that this data is lost in a case of a reboot or shutdown of the Raspberry Pi sensor. 

## Monitor Controller Instalation:

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
The installation of the Monitor Controller is relatively simple. Only a small amount of commands is required on the Raspberry PI:

```
apt-get git
git clone https://github.com/dennisshushack/BA_Thesis_PI.git
cd BA_Thesis_PI
chmod +x install_source.sh
./install_source.sh -s username@serveripaddress
```
Before launching the Monitor Controller, perform the following instructions on the Raspberry Pi sensor: 
```
cd BA_Thesis_PI/middleware
source env/bin/activate
```
## Commands:
Four commands are available to the User: Show, Collect, Send and Live.
The user will be prompted to input additional information, after activiating one of these commands. 

### Command Collect
For collecting training/evaluation data:
```
python3 cli.py collect
```
  
**Inputs**:

1. **Task Description**: A short description of your monitoring session.
2. **Type of Behavior**: Options (normal, poc=Ransomware-PoC, raas=RAASNet, dark=DarkRadiation) What are you monitoring? The normal State of the machine or the behavior during ransomware execution. -> Mainly needed for training Classification Algorithms.
3. **Category**: Is this data for training or evaluation/testing purposes?
4. **Monitoring duration**: The time to monitor in seconds.
5. **Monitoring Scripts to run in parallel**:  Which scripts do you want to run in parallel seperate by commas i.e: RES,KERN to run RES and KERN in parallalel. Minimum 1 monitoring script Required.
6. **Type of Machine Learning**: (Anomaly Detecection or Classfication)

Sample Input:
```
python3 cli.py collect
Please add a short description for this task: Training data gathering for anomaly detection
normal, poc, dark or raas (normal, poc, dark, raas): raas
Which category testing or training (training, testing): testing
time in seconds [3600]: 3600
Which monitors (i.e RES,KERN,SYS): RES,KERN,SYS
Server path (i.e root@194.233.160.46:/root/data): username@mypcip:/home/username/Desktop/data
Type anomaly or classification (anomaly, classification): classification
```

### Command Show
For viewing all past monitoring sessions:
```
python3 cli.py show
```

### Command Send:
For sending the metadata to the Data Anaylsis Application to start training/evaluating data
```
python3 cli.py send
```

### Command Live:
Starts a live monitoring session for 60 minutes
```
python3 cli.py live
```
