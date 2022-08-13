# Monitor Controller Repository File structure:
* `/monitors`: contains the monitoring scripts (RES, KERN and SYS)
* `/helpers`: contain the randomfile generator and ressource (CPU & Memory measuring script) with instructions
* `/middleware`: contains the actual middleware and controlls the monitoring scripts (KERN, RES and SYS)
* `install_source.sh`: To install all needed dependencies

This Repository is part of the thesis: 
Intelligent Framework to Detect Ransomware Affecting Linux-based and Resource-constrained Devices

If you have any troubles installing the Monitor Controller or other parts of the system feel free to contact me: dennis.shushack@uzh.ch



It is **highly** suggested to have a Linux or BSD based operating system running on your main machine. Mac OS should also work fine.
Windows on the other hand can be troublesome. If you run a Windows distribution, please consider dualbooting or installing a distro on an external SSD i.e. Ubuntu. It is also recommendet to have your machine connected via LAN and not WIFI, due to Network drops.

# Monitor Controller Instalation:

## Prerequisite:
You should have an ElectroSense sensor deployed and can SSH into it. 
You have a Linux/BSD based operating system running on your machine.

### Enabling SSH 
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



### Setup Pi

This setup is all you need to get the PI up and running. In the subdirectories a more specific explaination is given on the installation steps. Can be ignored otherwise.

As the monitor for system calls collects a large amount of data, I suggest having a server with at minimum 200gb of file storage available.

* Step 1: Flash the electrosense image on a SD card (i.e with rufus on Windows) on Linux use dd command of the unzipped file
* Step 2: Connect via ssh. `ifconfig` can help find the IP address of the Pi
* Step 3: ssh into the Pi
* Step 4: `vim  /etc/systemd/system/autossh-tunnel.service` Change number after -R to -R 20116
```
systemctl daemon-reload
service autossh-tunnel restart 
```
* Step 5: Update the system `apt-get update`
* Step 6: Install git `sudo apt-get install git`
* Step 7: Clone this repo: `git clone https://github.com/dennisshushack/BA_Thesis_PI.git` to /root/
* Step 8: Use the provided install_source.sh or install.sh sctripts (install.sh are compiled binaries) . To get the localhost use ifconfig user = defined user on system.
```
cd BA_Thesis_PI
chmod +x install.sh
./install.sh -s (username@localhost)
or 
./install_source.sh -s (username@localhost)
```

To start monitoring:
