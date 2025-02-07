
FROM python:3.9.16-slim-bullseye as base

ARG LOCAL_TIME=America/Argentina/Cordoba

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

EXPOSE 8000
WORKDIR /srv/sdump

RUN rm /etc/localtime \
    && ln -s /usr/share/zoneinfo/$LOCAL_TIME /etc/localtime

RUN useradd -ms /bin/bash dumpserver

RUN apt-get -y update && apt-get install -y --no-install-recommends \
    pkg-config  gettext  libpq-dev \
    python3-pip python3-apt python3-ldap python3-wheel python-pip-whl  \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip

FROM base as builder

RUN apt-get -y update && apt-get install -y \
    libdbus-1-dev  libyaml-dev libyaml-dev \
    libldap2-dev libsasl2-dev \
    libjpeg-dev zlib1g-dev libgtk2.0-dev libgirepository1.0-dev \
    libcurl4-openssl-dev libssl-dev python-dev


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/lib/python2.7/site-packages /usr/local/lib/python2.7/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY container-build/sdump/entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY . ./

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "sdump.wsgi:application", "--bind",  ":8000", "--workers", "$GUNICORN_WORKERS", "--timeout", "$GUNICORN_TIMEOUT"]
