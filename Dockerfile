# docker build -t sdump:latest .

#FROM python:2.7.18-buster
FROM python:3.9.16-bullseye
#FROM python:3.3-slim
#FROM python:3.9-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y  pkg-config  libdbus-1-dev gettext libpq-dev libyaml-dev \
    git python-dev python3-pip python3-apt python3-ldap pkg-config \
    libpq-dev libyaml-dev libldap2-dev libsasl2-dev gettext \
    libjpeg-dev zlib1g-dev libgtk2.0-dev libgirepository1.0-dev \
    python3-wheel python-pip-whl \
    postgresql-client
# RUN apt-get install -y  pkg-config gettext libpq-dev libyaml-dev \
#     pkg-config gettext libpq-dev libyaml-dev \
#     libldap2-dev libsasl2-dev libjpeg-dev zlib1g-dev libgtk2.0-dev \
#     libgirepository1.0-dev libssl-dev libffi-dev python3-dev \
#     libxml2 libxslt1.1 \
#     procps libcairo2 libcairo2-dev
    



# RUN apt-get install -y libcairo2-dev libcairo2 \
#    pkg-config gettext libpq-dev libyaml-dev \
#    libldap2-dev libsasl2-dev libjpeg-dev zlib1g-dev libgtk2.0-dev \
#    libgirepository1.0-dev \
#    build-essential libssl-dev libffi-dev python-dev \
#    libxml2-dev libxslt1-dev \
#    procps python3-apt python3-cairo python3-cairo-dev \
#    python3-cffi python3-cairocffi 
# #   python-cairo python-cairo-dev \

   
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

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


CMD ["gunicorn", "sdump.wsgi:application", "--bind",  ":8000"]
