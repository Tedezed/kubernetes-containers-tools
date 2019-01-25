#!/usr/bin/env bash

addgroup phpbb --gid $GID
adduser --disabled-password --ingroup phpbb --gecos "" --uid $UID phpbb

if [ ! -f /var/www/html/key_no_drop  ]; then
	echo "First start..."
	cp -R /phpbb-base/* /var/www/html/
	chmod 775 -R /var/www/html
	chown www-data -R /var/cache/nginx
	chown www-data -R /var/www/html
	touch /var/www/html/key_no_drop
fi

echo "Starting php-fpm..."
php-fpm --allow-to-run-as-root >/dev/null 2>&1 &
sleep 1

echo "Run PHP..."
service php7.0-fpm start
service php7.0-fpm restart
service php7.0-fpm status

echo "Run nginx..."
nginx -g 'daemon off;'