FROM debian:9

ENV DEBIAN_FRONTEND="noninteractive" \
	DAYS="15"

ADD custom /mnt/custom

RUN apt-get update \
	&& apt-get install -y apt-transport-https \
		curl \
		wget \
		gnupg \
		python \
		git \
		jq \
		nano \
	&& curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
	&& touch /etc/apt/sources.list.d/kubernetes.list  \
	&& echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends \
		kubectl \
	&& apt-get autoclean -y \
    && apt-get clean -y \
    && apt-get autoremove -y \
    && rm -rf /usr/share/locale/* \
    && rm -rf /var/cache/debconf/*-old \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/doc/* \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/cache/apt/archives/* \
    && chmod +x -R /mnt/custom/entrypoint.d/*

RUN git clone https://github.com/Tedezed/kubernetes-resources.git

VOLUME ["/root/backups"]