import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-73y4!-fk_6x$66y2n38ce9k%14n=k#rf7_h*!iq0g+y+wlx3s7'

DEBUG = False

ALLOWED_HOSTS = ['rentuikg.vercel.app', '*']

INSTALLED_APPS = [
    'main',
    'anons',
    'storages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://neondb_owner:npg_dy7MiDHcEme2@ep-weathered-dawn-agn0uo4l-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require',
        conn_max_age=600
    )
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# !!! СТРОКУ STATICFILES_STORAGE МЫ УДАЛИЛИ ОТСЮДА, ЧТОБЫ НЕ БЫЛО КОНФЛИКТА !!!

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login' 

WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False

AWS_ACCESS_KEY_ID='DO8019V99Y84BA7E6T8B'
AWS_SECRET_ACCESS_KEY='eOEgWw5jKTDldfArQmZ66wS3NMWafnLpcdFP8F7G69M'
AWS_STORAGE_BUCKET_NAME='fideakg'
AWS_S3_REGION_NAME = 'ams3'
AWS_S3_ENDPOINT_URL = 'https://ams3.digitaloceanspaces.com'


AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_REGION_NAME}.digitaloceanspaces.com'

# УБИРАЕМ ACL из запросов, чтобы DO не ругался
AWS_DEFAULT_ACL = None                
AWS_QUERYSTRING_AUTH = False          # Убирает мусорные токены (?AWSAccessKeyId...) из URL
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_EXTRA_ARGS = {}                # Тут должно быть пусто!

# Конфигурация хранилищ
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "querystring_auth": False,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN,
            # Меняем None на 'public-read', чтобы файлы автоматически становились доступными
            "default_acl": "public-read",      
            "file_overwrite": False,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.StaticFilesStorage",
    },
}

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
    'ACL': 'public-read',  # Даем Spaces понять, что это публичный файл
}

# Внутри бакета файлы летят в папочку media
AWS_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'