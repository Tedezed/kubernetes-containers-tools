#!/bin/bash

echo "v 0.0.2"
echo "User: $(whoami)"
echo $(export | grep "NAGIOS")
#echo "$(hostname)" >> /etc/apache2/httpd.conf

# Conf
chown -R nagios /etc/nagios3/custom

cp /files/conf/nagios/nagios.cfg /etc/nagios3/nagios.cfg
cp /files/conf/nagios/cgi.cfg /etc/nagios3/cgi.cfg
cp /files/conf/apache/000-default.conf /etc/apache2/sites-enabled/000-default.conf

sed -i "s/NAGIOS_USER/$NAGIOS_USER/g" /etc/nagios3/cgi.cfg

htpasswd -b -c /etc/nagios3/htpasswd.users $NAGIOS_USER $NAGIOS_PASS
chown www-data:nagios /etc/nagios3/htpasswd.users
chmod 440 /etc/nagios3/htpasswd.users

# Start apache2
#source /etc/apache2/envvars
#/usr/sbin/apache2 -X &
service apache2 start

# Start Nagios
#/usr/sbin/nagios3 -d /etc/nagios3/nagios.cfg &
service nagios3 start

# Start control-daemon apache2 nagios3
/files/executables/control-daemon.sh /var/run/apache2/apache2.pid /var/run/nagios3/nagios3.pid