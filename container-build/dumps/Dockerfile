# docker build -f container-build/dumps/Dockerfile -t dumps:latest .

FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    openssh-client openssh-server \
    postgresql-client mariadb-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash dumpserver

RUN mkdir -p /srv/dumps &&  \
    chown -R dumpserver.www-data /srv/dumps && \
    chmod -R 765 /srv/dumps

EXPOSE 22 80

WORKDIR /

COPY container-build/dumps/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["bash"]
