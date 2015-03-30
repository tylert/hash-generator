#!/usr/bin/env bash

if [ ! -d venv ]; then
    exit
fi

source venv/bin/activate
python ${@} generate_hashes.py
