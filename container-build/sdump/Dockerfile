
FROM python:3.9.16-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN apt-get -y update && apt-get install -y \
    pkg-config libdbus-1-dev gettext libpq-dev libyaml-dev \
    git python-dev python3-pip python3-apt python3-ldap pkg-config \
    libpq-dev libyaml-dev libldap2-dev libsasl2-dev gettext \
    libjpeg-dev zlib1g-dev libgtk2.0-dev libgirepository1.0-dev \
    python3-wheel python-pip-whl libcurl4-openssl-dev libssl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

RUN useradd -ms /bin/bash dumpserver

WORKDIR /srv/sdump

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY container-build/sdump/entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY . ./

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "sdump.wsgi:application", "--bind",  ":8000"]
