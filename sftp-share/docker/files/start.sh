#!/bin/bash

for type in rsa dsa ecdsa ed25519; do
  if ! [ -e "/ssh/ssh_host_${type}_key" ]; then
    echo "/ssh/ssh_host_${type}_key not found, generating..."
    ssh-keygen -f "/ssh/ssh_host_${type}_key" -N '' -t ${type}
  fi

  ln -sf "/ssh/ssh_host_${type}_key" "/etc/ssh/ssh_host_${type}_key"
done

if [ $MODE = 'CREATE_DB' ]; then
	for user in ${LIST_USERS[@]}
	do
		array=(${user//:/ }) # split
		USER=${array[0]}
		PASS=${array[1]}
		DIR=${array[2]}
		if ( id ${USER} ); then
		    echo "INFO: User ${USER} already exists"
		else
		    echo "INFO: User ${USER} does not exists, we create it"
		    ENC_PASS=$(perl -e 'print crypt($ARGV[0], "password")' ${PASS})
		    useradd -d $DIR -m -p ${ENC_PASS} -u ${USER_UID} -s /bin/sh ${USER}
		    USER_UID=$((USER_UID+1))
		fi
	done
else
	if ( id ${USER} ); then
		echo "INFO: User ${USER} already exists"
	else
		echo "INFO: User ${USER} does not exists, we create it"
		ENC_PASS=$(perl -e 'print crypt($ARGV[0], "password")' ${PASS})
		useradd -d $DIR -m -p ${ENC_PASS} -u ${USER_UID} -s /bin/sh ${USER}
		USER_UID=$((USER_UID+1))
	fi
fi

exec /usr/sbin/sshd -D
