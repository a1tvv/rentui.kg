#!/bin/bash

echo "Building the project..."
python3.9 -m pip install -r requirements.txt

# Важно: указываем ту же папку, что в settings.py и vercel.json
python3.9 manage.py collectstatic --noinput --clear

echo "Build Finished!"