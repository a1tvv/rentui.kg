#!/bin/bash

# Устанавливаем зависимости
pip install -r requirements.txt

# Собираем статику. 
# ВАЖНО: используем python3, так как Vercel понимает эту команду
python3 manage.py collectstatic --noinput --clear

echo "Билд завершен успешно!"