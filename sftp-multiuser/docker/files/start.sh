#!/bin/bash

set -x

### Functions ###

function fun_check_user {
	if ( id ${USER} ); then
		echo "INFO: User ${USER} already exists"
	else
		echo "INFO: User ${USER} does not exists, we create it"
		#ENC_PASS=$(perl -e 'print crypt($ARGV[0], "password")' ${PASS})
		useradd -d $DIR -m -p "$PASS" -u ${USER_UID} -s ${SHELL} ${USER}
		USER_UID=$((USER_UID+1))
	fi

	echo "INFO: Reset permissions..."
	chown $OWNER -R $DIR
	chmod g+rw -R $DIR
	chgrp $USER -R $DIR

	echo "INFO: Reset pass..."
	echo "$USER:$PASS"|chpasswd
}

function fun_gcsfuse {
	gcsfuse -o nonempty -o allow_other --dir-mode 770 --file-mode 760 --uid $OWNER_UID --gid $(id -u $USER) $BUCKET_NAME $DIR
}

### Functions ###

for type in rsa dsa ecdsa ed25519; do
  if ! [ -e "/ssh/ssh_host_${type}_key" ]; then
    echo "/ssh/ssh_host_${type}_key not found, generating..."
    ssh-keygen -f "/ssh/ssh_host_${type}_key" -N '' -t ${type}
  fi

  ln -sf "/ssh/ssh_host_${type}_key" "/etc/ssh/ssh_host_${type}_key"
done

# Check mode for users
if [ $MODE = 'user_list' ]; then

	chmod 400 $SFTP_MULTIUSER_FILE

	for line in $(cat $SFTP_MULTIUSER_FILE) ; do
		array=(${line//:/ }) # split
		USER=${array[0]}
		PASS=${array[1]}
		OWNER=${array[2]}
		DIR=${array[3]}

		fun_check_user
	done
elif [ $MODE = 'user_list_gcsfuse' ]; then

	chmod 400 $SFTP_MULTIUSER_FILE
	chmod 400 $GOOGLE_APPLICATION_CREDENTIALS

	for line in $(cat $SFTP_MULTIUSER_FILE) ; do
		array=(${line//:/ }) # split
		USER=${array[0]}
		PASS=${array[1]}
		OWNER=${array[2]}
		DIR=${array[3]}
		BUCKET_NAME=${array[4]}

		fun_check_user
		fun_gcsfuse
	done
else
	fun_check_user
fi

# gcsfuse
if [ $MODE = 'gcsfuse' ]; then
	chmod 400 $GOOGLE_APPLICATION_CREDENTIALS
	fun_gcsfuse
fi


exec /usr/sbin/sshd -D
