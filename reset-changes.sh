#!/bin/bash
date
echo Resetting tracked files to last known states.
cd /home/pi/Dev/BoogioBaseStation/
git reset --hard
echo done.
