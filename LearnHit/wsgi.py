import os
import environ
from django.core.wsgi import get_wsgi_application
from pathlib import Path

env = environ.Env(
	DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

environment = env('ENV')


if environment is not None and environment == "development":
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnHit.settings.dev')
else:
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnHit.settings.heroku')

application = get_wsgi_application()
