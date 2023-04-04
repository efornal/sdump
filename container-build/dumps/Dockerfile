# docker build -t dumps:latest .

FROM debian:bullseye-slim

WORKDIR /

RUN apt-get -y update
RUN apt-get install -y openssh-client openssh-server
RUN apt-get install -y postgresql-client mariadb-client

EXPOSE 22

#RUN adduser dumpserver
RUN useradd -ms /bin/bash dumpserver

RUN mkdir -p /srv/dumps/disa/esporadicos/
RUN mkdir -p /srv/dumps/wordpress/esporadicos/
RUN chmod -R 777 /srv/dumps

COPY container-build/dumps/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["bash"]
