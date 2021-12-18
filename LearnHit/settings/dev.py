import os

from LearnHit.settings.base import *
from LearnHit.settings.base import INSTALLED_APPS

ALLOWED_HOSTS = ['localhost', 'testserver']

DEBUG = True

SECRET_KEY = os.environ.get('LEARNHIT_DJANGO_SECRET_KEY');


# INSTALLED_APPS += ['django_extensions']

# ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

# NextJs Frontend Settings

NEXTJS_BASE_URL = "http://localhost:3000"
NEXTJS_EMAIL_CONFIRMATION_URL = f"{NEXTJS_BASE_URL}/account/confirm/email"
NEXTJS_PASSWORD_RESET_URL = f"{NEXTJS_BASE_URL}/account/password/reset/confirm"


# AllAuth Settings
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = f"{NEXTJS_BASE_URL}/account/login/";

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Cors Header Settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True


# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        'rest_framework.permissions.IsAuthenticated',
    ),
    "NON_FIELD_ERRORS_KEY": 'error',
}
