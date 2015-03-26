#!/usr/bin/env bash

if [ ! -d venv ]; then
    virtualenv venv
    source venv/bin/activate
    pip install --requirement requirements.txt
else
    source venv/bin/activate
fi

python generate_hashes.py
