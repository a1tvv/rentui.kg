#!/bin/bash

python3 -m ensurepip
python3 -m pip install --upgrade pip

# Ставим зависимости
python3 -m pip install -r requirements.txt

# Собираем статику
python3 manage.py collectstatic --noinput --clear