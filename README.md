# Roboface
## install
mkdir
sudo apt install python3-pip
sudo apt-get install python3-pip autoconf automake libtool aiy-python-wheels
curl https://raw.githubusercontent.com/ggravlingen/pytradfri/master/script/install-coap-client.sh | bash
cd libcoap
sudo make install

### Optional: Local python env:
sudo apt-get install python3-venv
python3 -m venv env
source env/bin/activate

### Python packages
pip3 install pytradfri
git clone https://github.com/google/aiyprojects-raspbian.git AIY-projects-python
sudo pip3 install -e AIY-projects-python/src

## Run
python3 face_detect_tradfri.py 192.168.9.164

## Running as service
``` 
# Create the symlink
sudo ln -s ~/roboface/face_detect_tradfri.service /lib/systemd/system

# Reload the service files so the system knows about this new one
sudo systemctl daemon-reload

# Now tell the system to run this service on bootup:
sudo systemctl enable face_detect_tradfri.service

#Or manually run it with this command:
sudo service face_detect_tradfri start

```
