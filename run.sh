#!/usr/bin/env bash

if [ ! -d venv ]; then
    echo 'Missing venv, please run setup'
    exit 1
fi

source venv/bin/activate
python ${@} generate_hashes.py
