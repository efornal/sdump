# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Django settings for sdump project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ast
import environ
import ldap
import logging
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = os.environ.get('BASE_URL')
APPLICATION_NAME = os.environ.get('APPLICATION_NAME')
APPLICATION_DESC = os.environ.get('APPLICATION_DESC')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')

ADMINS = os.environ.get('ADMINS')


MANAGERS = os.environ.get('MANAGERS')


BASIC_AUTH_REALM = 'User Authentication'

# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jquery',
    'jquery_ui',
    'bootstrap_ui',
    'django_extensions',
    'bootstrap_themes',
    'app',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'app.middleware.ForceLangMiddleware',
)

ROOT_URLCONF = 'sdump.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': os.environ.get('DEBUG'),
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sdump.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD':  os.environ.get('DB_USER_PASSWORD'),
        'PORT': os.environ.get('DB_PORT'),
        'HOST': os.environ.get('DB_HOST'),
    },
    'db_owner': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_OWNER'),
        'PASSWORD': os.environ.get('DB_OWNER_PASSWORD'),
        'PORT': os.environ.get('DB_PORT'),
        'HOST': os.environ.get('DB_HOST'),
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE =  os.environ.get('LANGUAGE_CODE')

LANGUAGES = (
  ('es', _('Spanish')),
  ('en', _('English')),
)

TIME_ZONE = os.environ.get('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_CHARSET = 'utf-8'

# Database engine options for server
ENGINE_OPTIONS = {{ engine_options }}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.environ.get('STATIC_ROOT')
STATIC_URL = os.environ.get('STATIC_URL')

LOGIN_URL = os.environ.get('LOGIN_URL')
LOGIN_REDIRECT_URL = os.environ.get('LOGIN_REDIRECT_URL')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

SUIT_CONFIG = {
    'ADMIN_NAME': APPLICATION_NAME
}

LOCALE_PATHS = [
    os.path.join(os.environ.get('CONTEXT_PATH'), '/shared/app/locale/'),
    os.path.join(BASE_DIR, 'locale/'),
]

SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME')
SESSION_COOKIE_PATH = "/"


# LDAP Configuration ==============/
LDAP_SERVER = os.environ.get('LDAP_SERVER')

LDAP_DN = os.environ.get('LDAP_BIND_DN')

# Organizational Unit for Person
LDAP_PEOPLE = os.environ.get('LDAP_PEOPLE')
LDAP_GROUP  = os.environ.get('LDAP_GROUP')

LDAP_DN_AUTH_USERS = os.environ.get('LDAP_DN_AUTH_USERS')
LDAP_DN_AUTH_GROUP = os.environ.get('LDAP_DN_AUTH_GROUP')

# =================================/


# =================================\
# django ldap configuration
#
#
# Ldap Group Type
from django_auth_ldap.config import LDAPSearch, PosixGroupType
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(LDAP_DN_AUTH_GROUP,
                                    ldap.SCOPE_SUBTREE, "(objectClass=posixGroup)"
)
AUTH_LDAP_GROUP_TYPE =  PosixGroupType()
#
#
# User will be updated with LDAP every time the user logs in.
# Otherwise, the User will only be populated when it is automatically created.
AUTH_LDAP_ALWAYS_UPDATE_USER = True
#
#
# Simple group restrictions
# AUTH_LDAP_REQUIRE_GROUP = "cn=users,ou={},{}".format(LDAP_GROUP,LDAP_DN)
# AUTH_LDAP_DENY_GROUP = "cn=denygroup,ou={},{}".format(LDAP_GROUP,LDAP_DN)
#
# Defines the django admin attribute
# according to whether the user is a member or not in the specified group
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=users,{}".format(LDAP_DN_AUTH_GROUP),
    "is_staff": "cn=users,{}".format(LDAP_DN_AUTH_GROUP),
    "is_superuser": "cn=admin,{}".format(LDAP_DN_AUTH_GROUP),
}
#
# Ldap User Auth
#AUTH_LDAP_BIND_DN = "cn={},{}".format(LDAP_USERNAME,LDAP_DN)
#AUTH_LDAP_BIND_PASSWORD = LDAP_PASSWORD

AUTH_LDAP_SERVER_URI = LDAP_SERVER

AUTH_LDAP_USER_SEARCH = LDAPSearch(LDAP_DN_AUTH_USERS,
                                   ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# CUSTOM CONFIGURATION OF APPLICATION ==============/

SHOW_DUMP_ERRORS_TO_USER = True

# Enable admin form button to verify connection
DATABASE_CONNECTION_VERIFICATION = os.getenv("DATABASE_CONNECTION_VERIFICATION", "False") == "True"

# Contains the configuration of connection to the service
# that provides the keys according to its id
# e.g.
# rattic_service_url: http://the_url_to_service
# rattic_service_creds: ('rattic_name','rattic_api_key')
RATTIC_SERVICE_URL = os.environ.get('RATTIC_SERVICE_URL')
RATTIC_SERVICE_CREDS = os.environ.get('RATTIC_SERVICE_CREDS')

# backups
DUMPS_DIRECTORY = os.environ.get('DUMPS_DIRECTORY')
GROUP_DUMPS_DIRECTORY = os.environ.get('GROUP_DUMPS_DIRECTORY')
USER_DUMPS_DIRECTORY  = os.environ.get('USER_DUMPS_DIRECTORY')
PERMISSIONS_DUMPS_DIRECTORY = os.environ.get('PERMISSIONS_DUMPS_DIRECTORY')
SUFFIX_PERIODICAL_DUMPS = os.environ.get('SUFFIX_PERIODICAL_DUMPS')
SUFFIX_SPORADIC_DUMPS = os.environ.get('SUFFIX_SPORADIC_DUMPS')
MAX_SPORADICS_BACKUPS = os.environ.get('MAX_SPORADICS_BACKUPS')
DUMPS_SCRIPT = os.environ.get('DUMPS_SCRIPT')
# for configurations dumps
DUMPS_CONFIG_DIRECTORY = os.environ.get('DUMPS_CONFIG_DIRECTORY')
PERMISSIONS_CONFIG_DUMP_FILE = os.environ.get('PERMISSIONS_CONFIG_DUMP_FILE')
DUMPS_CONFIG_AUTHENTICATION = os.environ.get('DUMPS_CONFIG_AUTHENTICATION')
DUMP_TIMEOUT = os.environ.get('DUMP_TIMEOUT')
#
# views
USER_NOTIFICATION = os.environ.get('USER_NOTIFICATION')
DEFAULT_CHARSET = os.environ.get('DEFAULT_CHARSET')


# ==================================================/
