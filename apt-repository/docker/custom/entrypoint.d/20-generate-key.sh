#!/bin/bash
set -e

cd /root

if [ ! -e /root/.gnupg/pubring.kbx ]; then
	echo "Key-Type: $PGP_TYPE
	Key-Length: $PGP_LENGTH
	Subkey-Type: $PGP_SUB_TYPE
	Subkey-Length: $PGP_SUB_LENGTH
	Name-Real: $PGP_REAL_NAME
	Name-Email: $PGP_EMAIL
	Expire-Date: $PGP_EXPIRE
	Passphrase: $PGP_PASSWD
	" >  /root/gen-key-script

	gpg --batch --gen-key gen-key-script
	gpg --armor --output /var/packages/$APT_DOMAIN.gpg.key \
	--export $(gpg --list-secret-keys --with-colons --fingerprint | grep ssb | cut -d ":" -f 5)
fi

gpg --list-keys
gpg --list-signatures


exit 0