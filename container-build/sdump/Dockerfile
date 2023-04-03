# docker build -t sdump:latest .

#FROM python:2.7.18-buster
FROM python:3.9.16-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y  pkg-config  libdbus-1-dev gettext libpq-dev libyaml-dev \
    git python-dev python3-pip python3-apt python3-ldap pkg-config \
    libpq-dev libyaml-dev libldap2-dev libsasl2-dev gettext \
    libjpeg-dev zlib1g-dev libgtk2.0-dev libgirepository1.0-dev \
    python3-wheel python-pip-whl
    
# temporal
RUN apt-get install -y  iputils-ping net-tools telnet

RUN pip install --upgrade pip
WORKDIR /srv/sdump
EXPOSE 8000

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get clean && apt-get autoremove

COPY app app
COPY sdump sdump
COPY LICENSE .
COPY locale locale
COPY manage.py .
COPY README.md .
COPY static static
COPY templates templates
COPY tests tests

COPY ./container-build/sdump/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# conf para ssh a contenedor de dumps
#RUN mkdir /root/.ssh && chmod 700 /root/.ssh
#COPY ./container-build/id_rsa /root/.ssh/
#COPY ./container-build/ssh_config /root/.ssh/config


CMD ["gunicorn", "sdump.wsgi:application", "--bind",  ":8000"]
