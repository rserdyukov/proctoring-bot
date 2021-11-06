#!/bin/bash

pip3 install -r requirements.txt

cd ../sources || { echo "Bot doesn't exist"; exit 1; }
python3 main.py