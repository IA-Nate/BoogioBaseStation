#/bin/bash
date
echo Running streaming demo
cd ~/Dev/BoogioBaseStation/Python/
sudo python3 streaming.py -c -p 20131 -b dc:80:07:ef:8b:cf
echo done.
