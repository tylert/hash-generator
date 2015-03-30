#!/usr/bin/env bash

#sudo easy_install pip
#sudo pip install virtualenv
#... or...
#sudo apt-get install python-pip python3-pip
#sudo apt-get install python-virtualenv python3-virtualenv

if [ ! -d venv ]; then
    virtualenv venv
    source venv/bin/activate
    pip install --requirement requirements.txt
else
    source venv/bin/activate
    pip install --upgrade --requirement requirements.txt
fi

#virtualenv venv3 --python=$(which python3)
#source venv3/bin/activate
#pip3 install --requirement requirements.txt
