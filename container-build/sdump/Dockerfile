# docker build -f container-build/sdump/Dockerfile -t sdump:latest .

FROM python:3.9.16-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y upgrade && apt-get install -y \
    pkg-config  libdbus-1-dev gettext libpq-dev libyaml-dev \
    git python-dev python3-pip python3-apt python3-ldap pkg-config \
    libpq-dev libyaml-dev libldap2-dev libsasl2-dev gettext \
    libjpeg-dev zlib1g-dev libgtk2.0-dev libgirepository1.0-dev \
    python3-wheel python-pip-whl && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

RUN mkdir -p /srv/dumps.conf.d && chown -R www-data.www-data /srv/dumps.conf.d

WORKDIR /srv/sdump

EXPOSE 8000

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app app
COPY sdump sdump
COPY LICENSE .
COPY locale locale
COPY manage.py .
COPY README.md .
COPY static static
COPY templates templates
COPY tests tests

COPY container-build/sdump/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "sdump.wsgi:application", "--bind",  ":8000"]
