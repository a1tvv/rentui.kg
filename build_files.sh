#!/bin/bash

echo "Создаем виртуальное окружение..."
python3 -m venv venv
source venv/bin/activate

echo "Обновляем pip..."
python3 -m pip install --upgrade pip

echo "Устанавливаем зависимости из requirements.txt..."
python3 -m pip install -r requirements.txt

echo "Собираем статику..."
python3 manage.py collectstatic --noinput --clear

echo "Билд завершен!"