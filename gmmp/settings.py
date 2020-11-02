"""
Django settings for gmmp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import gettext_lazy as _
from os import environ as env
from pathlib import Path 
from dotenv import load_dotenv
import django.conf.global_settings as DEFAULT_SETTINGS

env_path = Path(".") / ".env/.env"
load_dotenv(dotenv_path=env_path)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.get("DJANGO_DEBUG", False) == 'True'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default=env.get("DATABASE_URL", "postgres://gmmp:gmmp@db:5432/gmmp")
    )
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = "tm-v^$krw+%-vk5-u31dpini-e5dw(mi_pk0%s5g$$m%xp(r+r"
else:
    SECRET_KEY = env.get("DJANGO_SECRET_KEY")

COUNTRY_USER_DEFAULT_PASSWORD = env.get("COUNTRY_USER_DEFAULT_PASSWORD")
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "gmmp",
    "jet.dashboard",
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "guardian",
    "django_countries",
    "gsheets",
    "forms",
    "reports",
    "sheets",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]

ANONYMOUS_USER_NAME = None
GUARDIAN_RAISE_403 = True

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ROOT_URLCONF = 'django.urls'
ROOT_URLCONF = "gmmp.urls"

WSGI_APPLICATION = "gmmp.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("English")),
    ("es", _("Spanish")),
    ('fr', _('French')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = "../staticfiles"
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


SITE_URL = env.get('SITE_URL', 'http://localhost:8000')


# Temporary login screen for downloading the exported data
LOGIN_URL = "/admin/login/"

# Email
EMAIL_FROM = env.get("GMMP_EMAIL_FROM", "webmaster@localhost")
EMAIL_HOST = env.get("GMMP_EMAIL_HOST", "smtp.sendgrid.net")
EMAIL_PORT = int(env.get("GMMP_EMAIL_PORT", "2525"))
EMAIL_HOST_USER = env.get("GMMP_EMAIL_HOST_USER", "apikey")
EMAIL_HOST_PASSWORD = env.get("GMMP_EMAIL_HOST_PASSWORD")

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        }
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "ERROR"},
        "reports": {"level": "INFO"},
        "django": {"level": "DEBUG" if DEBUG else "INFO",},
    },
}

from django.utils.translation import gettext_lazy as _

# Great Britain: https://en.wikipedia.org/wiki/ISO_3166-2:GB#Countries_and_province
COUNTRIES_OVERRIDE = {
    "BE": None,
    "QM": {'name': _('Belgium - French'), 'alpha3': 'WAL'}, # Wallonia
    "QN": {'name': _('Belgium - Flemish'), 'alpha3': 'VLG'},
    "UK": None,
    "QO": {'name': _('England'), 'alpha3': 'ENG'},
    "QP": {'name': _("Northern Ireland"), 'alpha3': 'NIR'},
    "QQ": {'name': _("Scotland"), 'alpha3': 'SCT'},
    "QR": {'name': _("Wales"), 'alpha3': 'WLS'},
    "XI": {'name': _("International"), 'alpha3': 'XIN'},
    "PS": {'name': _("Palestine"), 'alpha3': 'PSE'}
}

# https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#adminsite-attributes
ADMIN_SITE_SITE_HEADER = _("GMMP Database")
ADMIN_SITE_SITE_TITLE = "GMMP"
ADMIN_SITE_SITE_URL = None
ADMIN_SITE_INDEX_TITLE = "Dashboard"

# Django Jet Customizations - https://jet.readthedocs.io/en/latest/config_file.html
JET_DEFAULT_THEME = "light-blue"
JET_SIDE_MENU_COMPACT = True
JET_INDEX_DASHBOARD = "gmmp.dashboard.CustomIndexDashboard"
JET_SIDE_MENU_ITEMS = [
    {
        "label": _("Code"),
        "items": [
            {
                "label": _("Newspapers"),
                "url": {"type": "reverse", "name": "admin:forms_newspapersheet_add"},
                "permissions": ['forms.view_newspapersheet'],
            },
            {
                "label": _("Radio"),
                "url": {"type": "reverse", "name": "admin:forms_radiosheet_add"},
                "permissions": ['forms.view_radiosheet']
            },
            {
                "label": _("Television"),
                "url": {"type": "reverse", "name": "admin:forms_televisionsheet_add"},
                "permissions": ['forms.view_televisionsheet']
            },
            {
                "label": _("Internet"),
                "url": {"type": "reverse", "name": "admin:forms_internetnewssheet_add"},
                 "permissions": ['forms.view_internetnewssheet']
            },
            {
                "label": _("Twitter"),
                "url": {"type": "reverse", "name": "admin:forms_twittersheet_add"},
                "permissions": ['forms.view_twittersheet']
            },
        ],
    },
    {
        "label": _("Coded"),
        "items": [
            {"name": "forms.newspapersheet", "permissions": ['forms.view_newspapersheet']},
            {"name": "forms.radiosheet", "permissions": ['forms.view_radiosheet']},
            {"name": "forms.televisionsheet", "permissions": ['forms.view_televisionsheet']},
            {"name": "forms.internetnewssheet", "permissions": ['forms.view_internetnewssheet']},
            {"name": "forms.twittersheet", "permissions": ['forms.view_twittersheet']},
        ],
    },
    {
        "label": _("Access Control"),
        "items": [{"name": "auth.user", "permissions": ['auth.view_user']}, {"name": "auth.group", "permissions": ['auth.view_group']},],
    },
    {
        "label": _("General"),
        "app_label": "core",
        "items": [
            {"label": _("Help"), "url": "#"},
            {
                "label": _("Facebook Group"),
                "url": "https://www.facebook.com/groups/1601794946722112/",
                "url_blank": True,
            },
            {
                "label": _("Methodology Guides & Coding Tools"),
                "url": "http://whomakesthenews.org/gmmp-2020/media-monitoring/methodology-guides-and-coding-tools",
                "url_blank": True,
            },
        ],
    },
    {
        "label": _("Other Links"),
        "items": [
            {
                "label": _("Who Makes The News"),
                "url": "http://whomakesthenews.org/",
                "url_blank": True,
            },
            {
                "label": _("Facebook"),
                "url": "https://www.facebook.com/Global.Media.Monitoring.Project/",
                "url_blank": True,
            },
        ],
    },
]

# GSheets
GSHEETS = {
    'CLIENT_SECRETS': os.path.join(BASE_DIR, env.get("GSHEETS_CLIENT_SECRETS", ".env/credentials.json")),
}
GSHEETS_SPECIAL_QUESTIONS = {
    'SPREADSHEET_ID': env.get("GSHEETS_SPECIAL_QUESTIONS_SPREADSHEET_ID", "1dttFvgcmS4yYrioge2Awav5k65QSAlSd95bX9yCqjA0"),
    'SHEET_NAME': env.get("GSHEETS_SPECIAL_QUESTIONS_SHEET_NAME", "DATA"),
}
GSHEET_COUNTRY_USERS = {
    'SPREADSHEET_ID': env.get("GSHEETS_COUNTRY_USERS_SPREADSHEET_ID", "1FjdgUbuCg5oYxv6my1E0Hw5gF1yDsOGb8Frm1HIXX3E"),
    'SHEET_NAME': env.get("GSHEETS_COUNTRY_USERS_SHEET_NAME", "DATA"),
}
