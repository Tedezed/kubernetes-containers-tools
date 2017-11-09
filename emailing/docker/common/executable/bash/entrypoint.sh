#!/bin/bash
set -e
#sleep 999999999

echo "v0.0.3"
echo "User: $(whoami)"
HOSTNAME="$(hostname)"
echo "Hostname: $HOSTNAME"

export HOSTNAME="$HOSTNAME"

echo $HOSTNAME > /etc/mailname

touch /var/spool/postfix/etc/resolv.conf && echo "nameserver 8.8.8.8
nameserver $DNS" > /var/spool/postfix/etc/resolv.conf

cp /mnt/common/conf/main.cf /etc/postfix/main.cf
cp /mnt/common/conf/sasl_passwd /etc/postfix/sasl_passwd

# Replace main.cf
sed -i -e "s/{{RELAYHOST}}/$RELAYHOST/g" /etc/postfix/main.cf
sed -i -e "s/{{RELAYHOST_PORT}}/$RELAYHOST_PORT/g" /etc/postfix/main.cf
sed -i -e "s/{{HOSTNAME}}/$HOSTNAME/g" /etc/postfix/main.cf
sed -i -e "s#{{NETWORKS}}#$NETWORKS#g" /etc/postfix/main.cf

# Replace sasl_passwd
sed -i -e "s/{{RELAYHOST}}/$RELAYHOST/g" /etc/postfix/sasl_passwd
sed -i -e "s/{{RELAYHOST_PORT}}/$RELAYHOST_PORT/g" /etc/postfix/sasl_passwd
sed -i -e "s/{{SMTP_KEY}}/$SMTP_KEY/g" /etc/postfix/sasl_passwd
sed -i -e "s/{{SMTP_SECRET}}/$SMTP_SECRET/g" /etc/postfix/sasl_passwd


postmap /etc/postfix/sasl_passwd
#ls -l /etc/postfix/sasl_passwd*
#rm /etc/postfix/sasl_passwd
chown root:root /etc/postfix/sasl_passwd*
chmod 600 /etc/postfix/sasl_passwd*
#ls -la /etc/postfix/sasl_passwd.db

postfix start
postfix reload
postfix stop
service syslog-ng start

#/mnt/common/executable/bash/control-daemon.sh /var/run/syslog-ng.pid /var/spool/postfix/pid/master.pid /usr/sbin/postfix start
/mnt/common/executable/bash/control-daemon.sh /var/run/syslog-ng.pid /var/spool/postfix/pid/master.pid postfix start

exit 1