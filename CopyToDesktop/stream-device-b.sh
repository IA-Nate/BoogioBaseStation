#/bin/bash
date
echo Running streaming demo
cd /home/pi/Dev/BoogioBaseStation/Python/
sudo python streaming.py -b dc:80:07:ef:8b:cf & sudo python streaming.py -b f5:47:18:cf:9c:dc
echo done.
