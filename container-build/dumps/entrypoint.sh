#!/usr/bin/env bash
set -e

if [[ -n ${DUMPSERVER_USER} && -n ${DUMPSERVER_PASSWORD} ]]; then
    echo -e ${DUMPSERVER_USER}:${DUMPSERVER_PASSWORD} | chpasswd
fi
# if [ id -u $DUMPSERVER_USER &>/dev/null ]; then
#     echo "ya existe, se omite usuario"
# else
#     echo "no existe"
#     useradd ${DUMPSERVER_USER}
#     echo -e ${DUMPSERVER_USER}:${DUMPSERVER_PASSWORD} | chpasswd
#     echo "creado"

# fi

service ssh restart 
tail -f /dev/null

exec "$@"
