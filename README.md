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
For collecting training/evaluation data. This data will be saved on your main machine. It is synced to your machine.
```
python3 cli.py collect
```
  
**Inputs**:

1. **Task Description**: A short description of your monitoring session.
2. **Type of Behavior**: Options (normal, poc=Ransomware-PoC, raas=RAASNet, dark=DarkRadiation) What are you monitoring? The normal State of the machine or the behavior during ransomware execution. -> Mainly needed for training Classification Algorithms.
3. **Category**: Is this data for training or evaluation/testing purposes?
4. **Monitoring duration**: The time to monitor in seconds.
5. **Monitoring Scripts to run in parallel**:  Which scripts do you want to run in parallel seperate by commas i.e: RES,KERN to run RES and KERN in parallalel. Minimum 1 monitoring script required.
6. **Path to save data**: A specified folder on your machine
7. **Type of Machine Learning**: (Anomaly detection or classfication)

Sample Input:
```
python3 cli.py collect
Please add a short description for this task: Testing data gathering for anomaly detection
normal, poc, dark or raas (normal, poc, dark, raas): raas
Which category testing or training (training, testing): testing
time in seconds [3600]: 20
Which monitors (i.e RES,KERN,SYS): RES,KERN,SYS
Server path (i.e root@194.233.160.46:/root/data): username@mypcip:/home/username/Desktop/data
Type anomaly or classification (anomaly, classification): anomaly
```
Sample Output:
```
Stopping Services if they are still running...
Starting Monitor Services and running it for 20 seconds
Please wait 20 seconds to start a new Monitoring Todo
  [####################################]  100%          
Finished montioring for 20.06 seconds.
Sending data to server  for monitor RES...
Data sent to server and deleted from local directory
Sending data to server  for monitor KERN...
Data sent to server and deleted from local directory
Sending data to server  for monitor SYS...
Data sent to server and deleted from local directory
Table for the device with the following cpu-id: 00000000fd4336c8
╒═════╤══════════════════════════════════════════════╤════════╤════════════╤═════════╤══════════════╤═══════════╤════════╤══════════╤════════════╤═════════════╕
│   # │ Description                                  │ Task   │ Category   │ Type    │ Monitors     │   Seconds │ Done   │ Sent     │      Added │   Completed │
╞═════╪══════════════════════════════════════════════╪════════╪════════════╪═════════╪══════════════╪═══════════╪════════╪══════════╪════════════╪═════════════╡
│   1 │ Testing data gathering for anomaly detection │ raas   │ testing    │ anomaly │ RES,KERN,SYS │        20 │ Done   │ Not Done │ 1660481675 │  1660481704 │
╘═════╧══════════════════════════════════════════════╧════════╧════════════╧═════════╧══════════════╧═══════════╧════════╧══════════╧════════════╧═════════════╛
```

### Command Show
For viewing all past monitoring sessions. No addition input required by the user.
```
python3 cli.py show
```
Shows the table as seen in the previous sample output.


### Command Send
For sending the metadata to the Data Anaylsis Application to start the training/evaluating procedure after collecting data. Can be called with `python3 cli.py send`. The index refers to # in the table. Note, do not send testing data to the server, if you have not trained the models yet. In the following example, the server already had the trained models ready to be evaluated. 

**Inputs**:
1. **Flask Application**: Refers to the ip + port of the flask application running. Make sure to set the IP of the FLask Application to your own IP (more detail in the Data Analyis Application section).
2. **Task Index**: Refers to the # column

Sample Input:
```
python3 cli.py send
Flask application i.e 127.0.0.1:5000: FlaskIP:5000
Task index: 1
```

Sample Output:
```
Sending following data of device 00000000fd4336c8 to server flaskip:5000...
############################################################
Task: raas
Description: Testing data gathering for anomaly detection 
Server: username@mypcip:/home/username/Desktop/data/00000000fd4336c8/anomaly/testing/Testing_data_gathering_for_anomaly_detection_/raas
Path: /home/username/Desktop/data/00000000fd4336c8/anomaly/testing
Monitors: RES,KERN,SYS
Category: testing
ML Type: anomaly
############################################################
Data sent to server
Table for the device with the following cpu-id: 00000000fd4336c8
╒═════╤══════════════════════════════════════════════╤════════╤════════════╤═════════╤══════════════╤═══════════╤════════╤════════╤════════════╤═════════════╕
│   # │ Description                                  │ Task   │ Category   │ Type    │ Monitors     │   Seconds │ Done   │ Sent   │      Added │   Completed │
╞═════╪══════════════════════════════════════════════╪════════╪════════════╪═════════╪══════════════╪═══════════╪════════╪════════╪════════════╪═════════════╡
│   1 │ Testing data gathering for anomaly detection │ raas   │ testing    │ anomaly │ RES,KERN,SYS │        20 │ Done   │ Done   │ 1660481675 │  1660481704 │
╘═════╧══════════════════════════════════════════════╧════════╧════════════╧═════════╧══════════════╧═══════════╧════════╧════════╧════════════╧═════════════╛

```


### Command Send:
For sending the metadata to the Data Anaylsis Application to start the training/evaluating procedure. The # column refers to the index:
```
python3 cli.py send
```
```



``


### Command Live:
Starts a live monitoring session for 60 minutes
```
python3 cli.py live
```
