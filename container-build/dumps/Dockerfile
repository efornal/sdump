
FROM debian:bookworm-slim

ARG LOCAL_TIME=America/Argentina/Cordoba

RUN rm /etc/localtime \
    && ln -s /usr/share/zoneinfo/$LOCAL_TIME /etc/localtime

RUN apt-get -y update && apt-get install -y --no-install-recommends \
    openssh-client openssh-server \
    postgresql-client mariadb-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash dumpserver

EXPOSE 22 80

WORKDIR /

COPY container-build/dumps/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["bash"]
