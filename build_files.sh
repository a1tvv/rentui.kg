#!/bin/bash

echo "Starting Build Process..."

# Используем curl для установки pip, если его нет, 
# или просто обновляем текущий
python3.9 -m ensurepip
python3.9 -m pip install --upgrade pip

# Устанавливаем все зависимости
python3.9 -m pip install -r requirements.txt

# Собираем статику
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear

echo "Build Finished!"