#!/bin/bash

set -x

export USER=$(sed ':a;N;$!ba;s/\n/ /g' <<< $USER)
export PASS=$(sed ':a;N;$!ba;s/\n/ /g' <<< $PASS)

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
	chmod 775 -R $DIR
	# SSH authorized_keys
	mkdir -p $DIR/.ssh
	touch $DIR/.ssh
	chmod 700 -R $DIR/.ssh
	chmod 600 -R $DIR/.ssh/authorized_keys
	chown $OWNER:$USER -R $DIR
	chown $USER $DIR
	chown $USER -R $DIR/.ssh

	if [ $MODE != 'user_list' ] && [ $MODE != 'user_list_gcsfuse' ]; then
		echo "INFO: Reset pass..."
		echo "$USER:$PASS"|chpasswd
	fi
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

#touch /var/log/sshd.log && tailf /var/log/sshd.log &
#exec /usr/sbin/sshd -E /var/log/sshd.log -d -D

while true;
do
	exec /usr/sbin/sshd -D
	sleep 3
done