#!/bin/bash
set -e

echo "ver 0.0.0.1"

#echo "$KMASTER kubernetes" >> /etc/hosts
echo "$KUBERNETES_SERVICE_HOST kubernetes" >> /etc/hosts
echo $ADD_HOST >> /etc/hosts

service rsyslog start

rm -rf /etc/nginx/sites-enabled/default

exec python /files/liberty-ingress/main.py time_query=$TIME_QUERY &

if [[ -v SECRET_USER ]];
then
	# Create htpasswd
	htpasswd -cb /etc/nginx/.htpasswd $SECRET_USER $SECRET_PASSWD
fi

echo "Exec Nginx"
exec nginx -c /etc/nginx/nginx.conf