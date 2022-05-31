# Files of Bachelor Thesis Dennis Shushack
# Setup the rasperry pi

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
* Step 7: Clone this repo: git clone https://github.com/dennisshushack/BA_Thesis_ds.git to /root/
* Step 8: Use the provided install.sh sctript. To get the localhost use ifconfig.
```
chmod +x install.sh
./install.sh -s (username@localhost)
```

Done!
