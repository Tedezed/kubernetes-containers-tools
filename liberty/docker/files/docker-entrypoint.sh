#!/bin/bash

# Ingress Controller Liberty
# Creator: Juan Manuel Torres
# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

set -e

echo "ver 1.2"

echo "Generate default cert..."
mkdir -p /files/liberty-ingress/certs/
mkdir -p /files/liberty-ingress/certs/kube-system_liberty-tls/
openssl req -x509 -nodes -days 100 \
   -subj "/CN=liberty-ingress.com" \
   -newkey rsa:1024 \
   -keyout /files/liberty-ingress/certs/kube-system_liberty-tls/tls.key \
   -out /files/liberty-ingress/certs/kube-system_liberty-tls/tls.crt \

echo "Configure system..."

#echo "$KMASTER kubernetes" >> /etc/hosts
echo "$KUBERNETES_SERVICE_HOST kubernetes" >> /etc/hosts
echo $ADD_HOST >> /etc/hosts
rm -rf /etc/nginx/sites-enabled/default

echo "Configure nginx..."
sed -i "s/SUPPORT_EMAIL/$SUPPORT_EMAIL/g" /files/error/index.html
sed -i "s/TEAM_NAME/$TEAM_NAME/g" /files/error/index.html

if [[ -v SECRET_USER ]];
then
	echo "Create htpasswd..."
	htpasswd -cb /etc/nginx/.htpasswd $SECRET_USER $SECRET_PASSWD
fi

echo "Exec rsyslog..."
service rsyslog start
echo "Exec Liberty..."
exec python /files/liberty-ingress/main.py time_query=$TIME_QUERY &
echo "Exec Nginx..."
exec nginx -c /etc/nginx/nginx.conf

echo "Bye Nginx-Liberty"
exit 1