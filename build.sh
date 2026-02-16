#!/bin/bash
pip install -r requirements.txt
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput