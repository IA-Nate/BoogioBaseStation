#/bin/bash
date
echo Running streaming demo
cd /home/pi/Dev/BoogioBaseStation/Python/
sudo python3 streaming.py -p 21030 -e -b f5:47:18:cf:9c:dc
echo done.
