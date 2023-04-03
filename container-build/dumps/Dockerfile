# docker build -t sdump_dumps:latest .

FROM debian:bullseye-slim

WORKDIR /

RUN apt-get -y update
RUN apt-get install -y openssh-client postgresql-client openssh-server
#RUN apt-get install -y sudo

EXPOSE 22

RUN adduser dumpserver


##RUN mkdir /root/.ssh && chmod 700 /root/.ssh
##COPY id_rsa.pub /root/.ssh/authorized_keys



#RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

#RUN ["service", "ssh", "restart"]

#COPY ./borrar_dumps_viejos /usr/local/sbin/borrar_dumps_viejos
#COPY ./hacer_backup /usr/local/sbin/hacer_backup
#COPY ./hacer_dumps_periodicos /usr/local/sbin/hacer_dumps_periodicos
#COPY ./funciones_basicas /usr/local/sbin/funciones_basicas
#COPY ./sudoers /etc/sudoers
#RUN chmod 755 /usr/local/sbin/*

RUN mkdir -p /srv/dumps/disa/esporadicos/
RUN chmod -R 777 /srv/dumps

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["bash"]
