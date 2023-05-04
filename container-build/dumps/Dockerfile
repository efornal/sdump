# docker build -f container-build/dumps/Dockerfile -t dumps:latest .

FROM debian:bullseye-slim

WORKDIR /

RUN apt-get -y update
RUN apt-get install -y openssh-client openssh-server
RUN apt-get install -y postgresql-client mariadb-client

EXPOSE 22 80

RUN useradd -ms /bin/bash dumpserver

COPY container-build/dumps/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["bash"]
