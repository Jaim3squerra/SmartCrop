#!/bin/bash

python3 -m venv smartcrop_venv
source smartcrop_venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
