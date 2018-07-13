FROM nginx:latest
MAINTAINER Juan Manuel Torres <juanmanuel.torres@aventurabinaria.es>

ENV DEBIAN_FRONTEND="noninteractive" \
	GID=1100

RUN cat /etc/issue \
	&& apt-get update \
    && apt-get install --no-install-recommends -y \
    	curl \
    	wget \
    	nano \
    	unzip \
    	php php-cgi php-fpm php-mysql php-xml php-gd \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's#listen = /run/php/php7.0-fpm.sock#listen = 127.0.0.1:9000#g' /etc/php/7.0/fpm/pool.d/www.conf \
	&& mkdir -p /var/www/html/ \
	&& mkdir -p /phpbb-base/

ENV VERSION_PHPBB="phpBB-3.2.1"
ENV DIR_PHPBB="phpBB3"

# PHPBB
RUN curl https://www.phpbb.com/files/release/${VERSION_PHPBB}.zip --insecure --output ${VERSION_PHPBB}.zip

# PHPBB languages
RUN curl https://www.phpbb.com/customise/db/download/145836 --insecure --output phpBB3-Spanish.zip

# Unzip phpBB
RUN unzip ${VERSION_PHPBB}.zip \
	&& mv ${DIR_PHPBB}/* /phpbb-base/ \
	&& rm -rf ${VERSION_PHPBB}.zip ${DIR_PHPBB}

# Unzip Languages phpBB
RUN unzip phpBB3-Spanish.zip \
	&& cp -r spanish_formal_honorifics_3_2_1/* /phpbb-base/ \
	&& rm -rf phpBB3-Spanish.zip spanish_formal_honorifics_3_2_1

COPY files/php-fpm.conf /usr/local/etc/
COPY files/nginx.conf /etc/nginx/conf.d/default.conf
COPY files/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
	&& chown -R www-data:www-data /var/www \
	&& chmod 660 /phpbb-base/images/avatars/upload/ /phpbb-base/config.php \
	&& chmod 770 /phpbb-base/store/ /phpbb-base/cache/ /phpbb-base/files/ \
	&& sed -i "s/upload_max_filesize = 2M/upload_max_filesize = 100M/g" /etc/php/7.0/cgi/php.ini \
	&& sed -i "s/post_max_size = 8M/post_max_size = 100M/g" /etc/php/7.0/cgi/php.ini

EXPOSE 80 443
VOLUME ["/var/cache/nginx", "/var/www/html/"]
ENTRYPOINT ["/entrypoint.sh"]