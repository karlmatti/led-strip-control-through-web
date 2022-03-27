#!/bin/bash
echo 'Starting to update project..'
git pull git@github.com:karlmatti/led-strip-control-through-web.git
echo 'Project updated!'
echo '#####################################################'
echo 'Starting the server..'
sudo python3 server.py

