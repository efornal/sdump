#!/usr/bin/env bash
set -e


if [ ! -d "/srv/dumps" ]; then
    echo "Inicializando /srv/dumps" && mkdir -vp /srv/dumps
else
    echo "/srv/dumps ya existe, ok!"
fi
chown -v dumpserver.www-data /srv/dumps


if [[ -n ${DUMPS_USER_NAME} && -n ${DUMPS_USER_PASS} ]]; then
    echo -e ${DUMPS_USER_NAME}:${DUMPS_USER_PASS} | chpasswd
    if [ $? -eq 0 ]; then
	echo -e "The password of user ${DUMPS_USER_NAME} has been updated."
    else
	echo -e "Error updating password of user ${DUMPS_USER_NAME}."
    fi
else
    echo -e "User ${DUMPS_USER_NAME} password update omitted, undefined data"
fi

service ssh restart 
tail -f /dev/null

exec "$@"
