#install
sudo apt install python3-pip
sudo apt-get install autoconf automake libtool
curl https://raw.githubusercontent.com/ggravlingen/pytradfri/master/script/install-coap-client.sh | bash
cd libcoap
sudo make install

# Lokal virtuell miljö:
#sudo apt-get install python3-venv
#python3 -m venv env
#source env/bin/activate

pip3 install pytradfri
sudo apt-get install -y aiy-python-wheels
git clone https://github.com/google/aiyprojects-raspbian.git AIY-projects-python
sudo pip3 install -e AIY-projects-python/src
python3 example_sync.py 192.168.9.164

python face_detect_tradfri.py
