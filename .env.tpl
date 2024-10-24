## django configuration

LANG=es_AR.UTF-8
TZ=America\/Argentina\/Cordoba

APPLICATION_NAME=Dumpserver
APPLICATION_DESC=Dumpserver

BASE_URL=https://0.0.0.0:3443

DEBUG=True

ALLOWED_HOSTS=['*']

ADMINS=(("admin", "admin@site.com"),)

MANAGERS=(("manager", "manager@site.com"),)

SECRET_KEY=the_secret_key

LANGUAGE_CODE=es

DEFAULT_CHARSET=utf-8

TIME_ZONE=America/Argentina/Buenos_Aires

CONTEXT_ROOT=/dumpserver

CONTEXT_PATH=/srv/sdump

LOGIN_URL=/dumpserver/login

LOGIN_REDIRECT_URL=/dumpserver

STATIC_ROOT=/srv/sdump/shared/static

STATIC_URL=/dumpserver/static/

SESSION_COOKIE_NAME=sdumpsessionid

LDAP_SERVER=ldap://host_ldap:389

LDAP_BIND_DN=dc=site,dc=edu,dc=ar
LDAP_BIND_USERNAME=username
LDAP_BIND_PASSWORD=password

LDAP_PEOPLE=People
LDAP_GROUP=Group

LDAP_GROUP_FIELDS=["gidNumber","cn"]
LDAP_PEOPLE_FIELDS=["uid","cn"]

LDAP_DN_AUTH_GROUP=ou=Group,dc=site,dc=unl,dc=ar
LDAP_DN_AUTH_USERS=ou=People,dc=site,dc=unl,dc=ar

LDAP_GROUP_VALIDATION=True
LDAP_GROUPS_VALID=["admin","others"]
LDAP_GROUP_MIN_VALUE=500
LDAP_GROUP_SKIP_VALUES=[666]
MIN_LENGTH_LDAP_USER_PASSWORD=8
LDAP_DEFAULT_GROUPS=["users","audio","cdrom"]

LDAP_PEOPLE_OBJECTCLASSES=["agente","hordeperson","inetOrgPerson","organizationalperson","person","posixaccount","shadowaccount","top","extensibleObject"]
LDAP_PEOPLE_PAISDOC="ARG"
LDAP_PEOPLE_HOMEDIRECTORY_PREFIX="/home/"
LDAP_PEOPLE_LOGIN_SHELL="/bin/bash"
LDAP_DOMAIN_MAIL="site.edu.ar"

DB_NAME=sdump_db
DB_USER=sdump_user
DB_USER_PASSWORD=db_user_password
DB_OWNER=db_owner
DB_OWNER_PASSWORD=db_owner_password
DB_HOST=db
DB_PORT=5432


RATTIC_SERVICE_URL=https://site_url
RATTIC_SERVICE_CREDS=('raticc_usr','rattic_key')

DUMPS_DIRECTORY=/srv/dumps
GROUP_DUMPS_DIRECTORY=www-data
USER_DUMPS_DIRECTORY =www-data
PERMISSIONS_DUMPS_DIRECTORY=0765
SUFFIX_PERIODICAL_DUMPS=periodicos
SUFFIX_SPORADIC_DUMPS=esporadicos
MAX_SPORADICS_BACKUPS=2
DUMPS_SCRIPT=/usr/local/sbin/hacer_backup
DUMPS_CONFIG_DIRECTORY=/srv/dumps.conf.d
PERMISSIONS_CONFIG_DUMP_FILE=0600
DUMPS_CONFIG_AUTHENTICATION=[id, username]
DUMP_TIMEOUT=60000
USER_NOTIFICATION=user_information_message

SESSION_COOKIE_NAME=produccionsdumpsessionid
SESSION_COOKIE_PATH=/

DUMPS_HOST_NAME=dumps
DUMPS_USER_NAME=dumpserver
DUMPS_USER_PASS=pass
