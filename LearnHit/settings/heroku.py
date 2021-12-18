import environ

from LearnHit.settings.base import *

env = environ.Env(
	DEBUG=(bool, False),
	CORS_ALLOW_CREDENTIALS=(bool, True)
)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

DATABASES = {
	'default': env.db(),
}

DEBUG = env('DEBUG')


# NextJs Frontend Settings

NEXTJS_BASE_URL = env('NEXTJS_BASE_URL')
NEXTJS_EMAIL_CONFIRMATION_URL = f"{NEXTJS_BASE_URL}/account/confirm/email"
NEXTJS_PASSWORD_RESET_URL = f"{NEXTJS_BASE_URL}/account/password/reset/confirm"

# AllAuth Settings
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = f"{NEXTJS_BASE_URL}/account/login/";

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')


SECRET_KEY = env('SECRET_KEY')


# Cors Header Settings
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_CREDENTIALS = env('CORS_ALLOW_CREDENTIALS')


# File Storage Settings
# DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DEFAULT_FILE_STORAGE = 'users.storage.CustomDropboxStorage'
DROPBOX_OAUTH2_TOKEN = env('DROPBOX_OAUTH_TOKEN')
DROPBOX_ROOT_PATH = '/'

