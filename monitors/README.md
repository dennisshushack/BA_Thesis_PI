# Monitor Scripts 

## Differences between the monitors:
* Monitor 1: Monitors HPC and Ressource usage -> Created in a BA Thesis 
* Monitor 2: Also monitors HPC & Ressource usage -> Created by Dr.Huertas
* Monitor 3: Monitors Systemcalls and is also part of a BA Thesis


## Setup of the Monitors:
For each of these monitor scripts a different systemd service needs to be created: `m1,m2,m3`.
Sample service files can be found in the service folder of this repository. Please copy the contents in the following files:
* For monitor 1: `vim /etc/systemd/system/m1.service`
* For monitor 2: `vim /etc/systemd/system/m2.service`
* For monitor 3: `vim /etc/systemd/system/m2.service`

## Requirements:
1. You will need Python 3 and python-venv installed: `sudo apt install python3-venv` 
2. You will need to make the two shell scripts of monitor 1 & monitor 2 executable `sudo chmod + x ./example.sh`

