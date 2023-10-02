#!/usr/bin/env bash
set -e

mkdir -p /srv/dumps.conf.d
mkdir -p /srv/dumps
chown -R www-data.www-data /srv/dumps.conf.d
chown -R www-data.www-data /srv/dumps

python manage.py compilemessages
python manage.py collectstatic --noinput
python manage.py migrate --database db_owner

exec "$@"
