#!/bin/bash

# Установка библиотек (включая whitenoise)
python3.9 -m pip install -r requirements.txt

# Сборка статики в папку /staticfiles
python3.9 manage.py collectstatic --noinput --clear