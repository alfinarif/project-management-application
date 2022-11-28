from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = config('SECRET_KEY')
DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # our apps
    'accounts',
    'projects',
    'leader',
    'worker',
    'payments',
    'admin_dashboard',
    'django_quill',
    
]


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
