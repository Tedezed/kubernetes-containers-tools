FROM tedezed/debian-box:latest
ENV DAYS_TO_DROP="32"
RUN apt-get update \
	&& apt-get install -y jq python-pip \
	&& mkdir /sa
ADD files /files
RUN mv /files/yq /usr/local/bin/yq \
	&& pip install yq
ENTRYPOINT ["/bin/bash", "/files/entrypoint.bash"]
