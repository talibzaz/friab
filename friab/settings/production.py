from .base import *

DEBUG = False

ALLOWED_HOSTS = ['talibzaz.pythonanywhere.com']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'metro_db',
        'USER': 'talibzaz',
        'PASSWORD': 'root',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
