"""
Django settings for gmmp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os import environ as env
import django.conf.global_settings as DEFAULT_SETTINGS

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.get('DJANGO_DEBUG', 'true') == 'true'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import dj_database_url

DATABASES = {'default' : dj_database_url.config(default=env.get('DATABASE_URL', 'postgres://gmmp:gmmp@db:5432/gmmp'))}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/



# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = 'tm-v^$krw+%-vk5-u31dpini-e5dw(mi_pk0%s5g$$m%xp(r+r'
else:
    SECRET_KEY = env.get('DJANGO_SECRET_KEY')

# DEBUG = True
#
# TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    'guardian',
    'forms',
    'gmmp',
    'django_countries',
    'reports',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1
GUARDIAN_RAISE_403 = True

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
)

ROOT_URLCONF = 'gmmp.urls'

WSGI_APPLICATION = 'gmmp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

#LANGUAGE_CODE = 'fr_fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = '../staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

GRAPPELLI_ADMIN_TITLE='<a href="/">Global Media Monitoring Project - 2015</a>'
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
    '/gmmp/forms/locale/',
]

# Temporary login screen for downloading the exported data
LOGIN_URL = '/admin/login/'


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'ERROR'
        },
        'reports': {'level': 'INFO'},
        'django': {
            'level': 'DEBUG' if DEBUG else 'INFO',
        }
    }
}

from django.utils.translation import ugettext_lazy as _

COUNTRIES_OVERRIDE = {
    'SQ': _('Scotland'),
    'EN': _('England'),
    'WL': _('Wales'),
    'B1': _('Belgium - French'),
    'B2': _('Belgium - Flemish')
}
