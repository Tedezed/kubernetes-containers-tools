#!/bin/bash
set -e

#gpg --list-keys --with-colons XXXXXXXX | awk -F: '/^pub:/ { print $5 }'
echo "Origin: $APT_DOMAIN
Label: $APT_DOMAIN
Codename: $APT_CODENAME
Architectures: $APT_ARCHITECTURES
Components: $APT_COMPONENTS
Description: $APT_DESCRIPTION
SignWith: $(gpg --list-secret-keys --with-colons --fingerprint | grep ssb | cut -d ":" -f 5)
DebOverride: $APT_DEBOVERRIDE
DscOverride: $APT_DSCOVERRIDE
" > /var/packages/debian/conf/distributions

touch /var/packages/debian/conf/$APT_DEBOVERRIDE

echo "verbose
ask-passphrase
basedir /var/packages/debian
" > /var/packages/debian/conf/options

#curl -SL http://ftp.us.debian.org/debian/pool/main/p/python3.7/python3.7_3.7.3-2+deb10u1_amd64.deb -o /usr/src/pagespeed/python3.7_3.7.3-2+deb10u1_amd64.deb
#export GPG_TTY=$(tty)
#dpkg-sig -k $(gpg --list-secret-keys --with-colons --fingerprint | grep ssb | cut -d ":" -f 5) --sign builder /usr/src/pagespeed/*.deb
#cd /var/packages/debian
#reprepro includedeb testing /usr/src/pagespeed/*.deb

exit 0
