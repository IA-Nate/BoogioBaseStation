#/bin/bash
date
echo Running streaming demo
cd ~/Dev/BoogioBaseStation/Python/
sudo python3 streaming.py -p 21030 -e -b dc:80:07:ef:8b:cf
echo done.
