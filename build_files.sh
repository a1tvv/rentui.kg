#!/bin/bash

# Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# Сбор статических файлов
python manage.py collectstatic --noinput --clear

# Миграции
python manage.py migrate --noinput