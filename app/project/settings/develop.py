"""
Django development settings for project.
"""

from environs import Env
from .base import *

# Load environment
env = Env()
env.read_env('.env')

# SECURITY WARNING: keep the secret key used in production secret!
APP_HOST = env('APP_HOST')
APP_PORT = env('APP_PORT')
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env('SQL_ENGINE'),
        'NAME': env('SQL_DATABASE'),
        'USER': env('SQL_USER'),
        'PASSWORD': env('SQL_PASSWORD'),
        'HOST': env('SQL_HOST'),
        'PORT': env('SQL_PORT'),
    }
}

PASSWORD_RESET_TIMEOUT = 24 * 60 * 60  # 24 hours, in seconds

# Rest

REST_FRAMEWORK['DEFAULT_FILTER_BACKENDS'] = ['django_filters.rest_framework.DjangoFilterBackend']

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

TIME_ZONE = 'Europe/Kiev'

# Email sending

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
