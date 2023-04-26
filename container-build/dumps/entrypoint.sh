#!/usr/bin/env bash
set -e

if [[ -n ${DUMPS_USER_NAME} && -n ${DUMPS_USER_PASSWORD} ]]; then
    echo -e ${DUMPS_USER_NAME}:${DUMPS_USER_PASSWORD} | chpasswd
fi

service ssh restart 
tail -f /dev/null

exec "$@"
