
FROM debian:bullseye-slim

RUN apt-get -y update && apt-get install -y \
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
