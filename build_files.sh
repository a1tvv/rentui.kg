pip install -r requirements.txt --break-system-packages
python3.12 manage.py collectstatic --noinput --clear
echo "BUILD END"