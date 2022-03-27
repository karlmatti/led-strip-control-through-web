#!/bin/bash
echo 'Starting to update project..'
git remote -v
git remote set-url origin git@github.com:karlmatti/led-strip-control-through-web.git
git pull git@github.com:karlmatti/led-strip-control-through-web.git
# sudo git pull 
echo 'Project updated!'
echo 'Starting the server..'
sudo python3 server.py

