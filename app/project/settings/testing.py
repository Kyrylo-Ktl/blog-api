"""
Django testing settings for project.
"""

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
APP_HOST = 'localhost'
APP_PORT = 8000
SECRET_KEY = 'super_secret_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email sending

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
