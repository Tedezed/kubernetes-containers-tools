FROM debian:stretch-slim

ENV DEBIAN_FRONTEND="noninteractive" \
	PGP_TYPE=1 \
	PGP_LENGTH=2048 \
	PGP_SUB_TYPE=1 \
	PGP_SUB_LENGTH=2048 \
	PGP_REAL_NAME="Sluagh" \
	PGP_EMAIL="example@exmaple.com" \
	PGP_EXPIRE=0 \
	PGP_PASSWD="example_passwd_12345" \
	APT_DOMAIN="apt.example.com" \
	APT_CODENAME="testing" \
	APT_ARCHITECTURES="amd64" \
	APT_COMPONENTS="main" \
	APT_DESCRIPTION="Example APT Repository" \
	APT_DEBOVERRIDE="override.testing" \
	APT_DSCOVERRIDE="override.testing" \
	DENY_EXTENSIONS="config|conf"

RUN apt-get update \
	&& apt-get install -y gnupg rng-tools nginx reprepro dpkg-sig curl nano \
	&& echo 'HRNGDEVICE=/dev/urandom' >> /etc/default/rng-tools

ADD custom /mnt/custom
RUN chmod +x /mnt/custom/executable/bash/entrypoint.sh

EXPOSE 80 443
VOLUME ["/root/.gnupg", "/usr/src/pagespeed", "/var/packages"]
ENTRYPOINT ["/mnt/custom/executable/bash/entrypoint.sh"]