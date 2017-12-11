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
    	php php-cgi php-fpm php-mysql \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's#listen = /run/php/php7.0-fpm.sock#listen = 127.0.0.1:9000#g' /etc/php/7.0/fpm/pool.d/www.conf

ENV VERSION_PHPBB="phpBB-3.2.1"
ENV DIR_PHPBB="phpBB3"

RUN curl https://www.phpbb.com/files/release/${VERSION_PHPBB}.zip --insecure --output ${VERSION_PHPBB}.zip
#RUN wget https://www.phpbb.com/files/release/${VERSION_PHPBB}.zip

RUN unzip ${VERSION_PHPBB}.zip \
	&& mkdir -p /var/www/html/ \
	&& mv ${DIR_PHPBB}/* /var/www/html/ \
	&& rm -rf ${VERSION_PHPBB}.zip ${DIR_PHPBB}

RUN mkdir -p /var/www/html/cache /var/www/html/store /var/www/html/files /var/www/html/images/avatars/upload/ \
	chown www-data:www-data /var/www/html/cache /var/www/html/store /var/www/html/files /var/www/html/images/avatars/upload/

COPY files/php-fpm.conf /usr/local/etc/
COPY files/nginx.conf /etc/nginx/conf.d/default.conf
COPY files/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
	&& chown -R www-data:www-data /var/www \
	&& chmod 660 /var/www/html/images/avatars/upload/ /var/www/html/config.php \
	&& chmod 770 /var/www/html/store/ /var/www/html/cache/ /var/www/html/files/

EXPOSE 80 443
VOLUME ["/var/cache/nginx", "/var/www/html/cache", "/var/www/html/store", "/var/www/html/files", "/var/www/html/images/avatars/upload/"]
ENTRYPOINT ["/entrypoint.sh"]