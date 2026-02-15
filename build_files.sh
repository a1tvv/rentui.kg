#!/bin/bash

# Устанавливаем зависимости, игнорируя блокировку среды
python3 -m pip install --break-system-packages -r requirements.txt

# Собираем статику
python3 manage.py collectstatic --noinput --clear

echo "Билд завершен!"