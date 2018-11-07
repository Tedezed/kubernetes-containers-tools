FROM debian:jessie
MAINTAINER Juan Manuel Torres (Tedezed) <juanmanuel.torres@aventurabinaria.es>

ENV KMASTER kubernetes \
	ADD_HOST "127.0.0.1 localhost" \
	NAMESPACE default \
	HEAPSTER url_heapster \
	AUTOSCALER_COUNT 10 \
	TIME_QUERY 17 \
	CONF_KUBE_BASE64 add

RUN apt-get update \
    && apt-get install -y \
        python2.7 \
        python-pip \
        git \
        nano \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pykube google-auth-oauthlib

ADD slug_statefulset_autoscaler/ /slug_statefulset_autoscaler
ADD files/docker-entrypoint.sh /usr/local/bin/

RUN chmod +rx /usr/local/bin/docker-entrypoint.sh

USER root
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/bin/bash"]