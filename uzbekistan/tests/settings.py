"""
Test settings for uzbekistan app.
"""

import os

SECRET_KEY = os.getenv('DJANGO_TEST_SECRET_KEY', 'test-key-not-for-production')
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'uzbekistan',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'uzbekistan.tests.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': None,
    'PAGE_SIZE': None,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = False  # Explicitly set to False to maintain current behavior

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

UZBEKISTAN = {
    'models': {
        'region': True,
        'district': True,
        'village': True,
    },
    'views': {
        'region': True,
        'district': True,
        'village': True,
    },
    'cache': {
        'enabled': False,
        'timeout': 3600,
    }
} 