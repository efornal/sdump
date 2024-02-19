#!/usr/bin/env bash
set -e


if [ ! -d "/srv/dumps.conf.d" ]; then
    echo "Inicializando /srv/dumps.conf.d" && mkdir -vp /srv/dumps.conf.d
else
    echo "/srv/dumps.conf.d ya existe, ok!"
fi
chown -v www-data.www-data /srv/dumps.conf.d


python manage.py compilemessages
python manage.py collectstatic --noinput
python manage.py migrate --database db_owner

exec "$@"
