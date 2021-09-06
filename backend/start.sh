#!/bin/bash
# python3 -m venv virtual-env
virtualenv virtual-env 
source virtual-env/bin/activate
pip3 install -r requirements.txt
# python3 server.py
flask run --host=0.0.0.0
