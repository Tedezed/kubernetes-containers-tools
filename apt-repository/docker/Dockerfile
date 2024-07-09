# STABLE
#FROM ubuntu:18.04

# LATEST
FROM debian:stable-slim

ENV DEBIAN_FRONTEND="noninteractive" \
	PGP_TYPE=1 \
	PGP_LENGTH=1024 \
	PGP_SUB_TYPE=1 \
	PGP_SUB_LENGTH=1024 \
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
	DENY_EXTENSIONS="config|conf" \
	APT_REPOSITORY="debian"

RUN apt-get update \
	&& apt-get install -y software-properties-common \
	# dpkg-sig
	&& apt-get install -y gpg gnupg gnupg2 gnupg-agent rng-tools nginx reprepro curl nano dpkg-dev \
	&& echo 'HRNGDEVICE=/dev/urandom' >> /etc/default/rng-tools

ADD custom /mnt/custom
RUN chmod +x /mnt/custom/executable/bash/entrypoint.sh \
	&& cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf_original

EXPOSE 80 443
USER root
VOLUME ["/root/.gnupg", "/usr/src/pagespeed", "/var/packages"]
ENTRYPOINT ["/mnt/custom/executable/bash/entrypoint.sh"]
