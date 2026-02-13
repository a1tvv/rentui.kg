import dj_database_url
import os

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3', # Оставляем для локальной разработки
        conn_max_age=600
    )
}