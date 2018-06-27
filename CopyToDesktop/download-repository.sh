#!/bin/bash
date
echo downloading repository...
cd /home/pi/Dev/
rm -rf BoogioBaseStation/
git clone https://github.com/IA-Nate/BoogioBaseStation.git
echo done.
