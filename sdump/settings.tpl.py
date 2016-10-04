# -*- encoding: utf-8 -*-
"""
Django settings for sdump project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from django.utils.translation import ugettext_lazy as _


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'clwt@lvpqw#f)&g*1f$2e+*!*pg($8jtpvmn5n&v8uds2l3-k='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'bootstrap_themes',
    'app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sdump.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
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
        'NAME': 'sdump_db',
        'USER': 'sdump_owner',
        'PASSWORD': 'owner',
        'PORT': '5432',
        'HOST': 'localhost',
    }
}

# =================================/
# APPLICATION configuration
#
# title displayed in the header
APPLICATION_NAME = "Sargo"
#
# directory dumps performed by the cron defined in DUMPS_SCRIPT
DUMPS_DIRECTORY = "/srv/dumps" 
#
# 
#
# permissions that apply to the directory created
GROUP_DUMPS_DIRECTORY = 'www-data'
USER_DUMPS_DIRECTORY  = 'www-data'
PERMISSIONS_DUMPS_DIRECTORY = '0765' # => drwxrw-r-x
#
# subdirectories dumps to discriminate
SUFFIX_PERIODICAL_DUMPS = "periodicos"
SUFFIX_SPORADIC_DUMPS = "esporadicos"
#
# Maximum number of dump that the system can contain.
# A message to the user is given if Exed that amount
MAX_SPORADICS_BACKUPS = 5
#
# directory configuration files each dump to be performed by the cron
# defined in DUMPS_SCRIPT
DUMPS_CONFIG_DIRECTORY = "/srv/dumps/dumps.conf.d"
PERMISSIONS_CONFIG_DUMP_FILE = '0600'
#
# by 'id' and/or 'username'. Ej, both of them: ['id', 'username']
DUMPS_CONFIG_AUTHENTICATION = ['id']
#
# bash script to make dump
DUMPS_SCRIPT = "/srv/scripts/hacer_dump"
#
#
# Message to the user on the home page
USER_NOTIFICATION = "a user notification..., perhaps "

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es'

LANGUAGES = (
  ('es', _('Spanish')),
  ('en', _('English')),
)

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

LOGIN_URL='/login/'
LOGIN_REDIRECT_URL = '/'

DEFAULT_CHARSET = 'utf-8'

SUIT_CONFIG = {
    'ADMIN_NAME': APPLICATION_NAME
}

LOCALE_PATHS = ( BASE_DIR + '/locale', )


# LDAP Configuration ==============/

# LDAP server
LDAP_SERVER = 'ldap://host_ldap:port'

# Dn for entry
LDAP_DN = 'dc=domain,dc=edu,dc=ar'

# LDAP authentication
#LDAP_USER_NAME='username'
#LDAP_USER_PASS='password'

# Organizational Unit for Person
LDAP_PEOPLE = 'People'

# =================================/


# =================================\
# django ldap configuration

import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

import logging
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


AUTH_LDAP_SERVER_URI = LDAP_SERVER

#AUTH_LDAP_BIND_DN = "cn=%s,%s" % ( LDAP_USER_NAME, LDAP_DN )
#AUTH_LDAP_BIND_PASSWORD = LDAP_USER_PASS

AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=%s,%s" % (LDAP_PEOPLE,LDAP_DN),
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
