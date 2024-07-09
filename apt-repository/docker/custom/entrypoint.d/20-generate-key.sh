#!/bin/bash
set -xe

cd /root

GPG_CONF="Key-Type: $PGP_TYPE
Key-Length: $PGP_LENGTH
Subkey-Type: $PGP_SUB_TYPE
Subkey-Length: $PGP_SUB_LENGTH
Name-Real: $PGP_REAL_NAME
Name-Email: $PGP_EMAIL
Expire-Date: $PGP_EXPIRE
Passphrase: $PGP_PASSWD"

if [ ! -e /root/.gnupg/pubring.kbx ]; then
	echo "${GPG_CONF}" >  /root/gen-key-script
	
	# Check if gpg is already running
	n=0
	until [ "$n" -ge 6 ]
	do
		gpg-connect-agent /bye && break
		n=$((n+1)) 
		sleep 1
	done

	gpg --batch --gen-key gen-key-script
	gpg --list-secret-keys --with-colons --fingerprint 
	gpg --armor --output /var/packages/$APT_DOMAIN.gpg.key \
	--export $(gpg --list-secret-keys --with-colons --fingerprint | grep ssb | cut -d ":" -f 5)
fi

gpg --list-keys
gpg --list-signatures


exit 0