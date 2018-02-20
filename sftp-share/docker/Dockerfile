FROM ubuntu:14.04
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

ENV USER_UID 1001

ENV MODE="one_user" \
	USER="ted" \
	PASS="tedpass" \
	DIR="/data/demo" \
	OWNER="www-data"

ENV MODE="user_list" \
	LIST_USERS="admin:admin:/data ted:ted2:/data/demo"

ENV DI_VERSION 1.0.1
ENV DI_HASH 91b9970e6a0d23d7aedf3321fb1d161937e7f5e6ff38c51a8a997278cc00fb0a

ADD https://github.com/Yelp/dumb-init/releases/download/v1.0.1/dumb-init_${DI_VERSION}_amd64 /usr/local/bin/dumb-init

RUN apt-get update \
 && apt-get install -y openssh-server mcrypt nano build-essential \
 && mkdir /var/run/sshd && chmod 0755 /var/run/sshd \
 && echo "${DI_HASH}  /usr/local/bin/dumb-init" | sha256sum -c \
 && chmod +x /usr/local/bin/dumb-init

# Clean
ENV SUDO_FORCE_REMOVE=yes
RUN apt-get remove -y --purge --auto-remove nano vim iputils-ping pico sudo
RUN echo 'Yes, do as I say!' | apt-get remove -y --purge --auto-remove --force-yes vim-common vim-tiny wget util-linux make gcc g++ fakeroot


RUN cd / && chmod -R o=-rwx /.dockerenv
#RUN chmod -R o=-rwx `ls / | grep -v "sys\|proc"` && chmod o=+rx /bin/sh
RUN sed -i -e "s/DIR_MODE=0755/DIR_MODE=0750/g" /etc/adduser.conf

ADD files/start.sh /usr/local/bin/start.sh
ADD files/sshd_config /etc/ssh/sshd_config

VOLUME ["/data", "/ssh"]
EXPOSE 22

ENTRYPOINT ["/usr/local/bin/dumb-init"]
CMD ["/usr/local/bin/start.sh"]
