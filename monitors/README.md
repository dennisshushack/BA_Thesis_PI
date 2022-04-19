# Monitor Scripts 

## Differences between the monitors:
* Monitor 1: Monitors HPC and Ressource usage -> Created in a BA Thesis 
* Monitor 2: Also monitors HPC & Ressource usage -> Created by Dr.Huertas
* Monitor 3: Monitors Systemcalls and is also part of a BA Thesis


## Setup of the Monitors:
For each of these monitor scripts a different systemd service needs to be created: `m1,m2,m3`
For each of the files a sample .service file can be found in the service folder
* For monitor 1: `vim /etc/systemd/system/m1.service`
* For monitor 2: `vim /etc/systemd/system/m2.service`




