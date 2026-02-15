#!/bin/bash

# Устанавливаем зависимости
pip install -r requirements.txt

# Применяем миграции к базе Neon (КРИТИЧЕСКИЙ ШАГ)
python3.12 manage.py migrate --noinput

# Собираем статику
python3.12 manage.py collectstatic --noinput --clear

echo "Билд успешно завершен!"