# Files of Bachelor Thesis Dennis Shushack
* `/monitors`: contains the monitoring scripts
* `/helpers`: contains a random file generator (use on SSD) and a ressource monitor as binary or py file.
### Ressource Monitor
Measures CPU, Memory, Network & Reads, Writes writes them to a .csv and calculates the mean. Takes a directory + time as args.
For source:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
# Run the script for 10 seconds and save it in /tmp
python3 main.py /tmp 10
```

For binary:
```
chmod +x main
./main /tmp 10
```

```
# Setup Pi

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
* Step 7: Clone this repo: `git clone https://github.com/dennisshushack/BA_Thesis_ds.git` to /root/
* Step 8: Use the provided install_source.sh or install.sh sctripts (install.sh are compiled binaries) . To get the localhost use ifconfig user = defined user on system.
```
cd BA_Thesis_PI
chmod +x install.sh
./install.sh -s (username@localhost)
or 
./install_source.sh
```

To start monitoring:
