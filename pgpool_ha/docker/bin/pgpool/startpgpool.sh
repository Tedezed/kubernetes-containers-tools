#!/bin/bash

# Copyright 2015 Crunchy Data Solutions, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# clean up leftovers from previous runs of pgpool
rm -rf /tmp/pgpool.pid
rm -rf /tmp/.s.*

#env

function trap_sigterm() {
	echo "doing trap logic..."
	kill -SIGINT $PGPOOL_PID
}

trap 'trap_sigterm' SIGINT SIGTERM

#sudo sh -c "echo \"$PG_PRIMARY_IP   $PG_PRIMARY_SERVICE_NAME
#$PG_REPLICA_IP   $PG_REPLICA_SERVICE_NAME
#\" >> /etc/hosts"

# SSH
KEYS_PATH=${KEYS_PATH:-/home/daemon/.ssh}
PRIVATE_KEY=$KEYS_PATH/id_rsa
PUBLIC_KEY=${PRIVATE_KEY}.pub

if [ ! -f "$PRIVATE_KEY" ]; then
  sudo chown -R daemon:daemon $KEYS_PATH
  /usr/bin/ssh-keygen -q -t rsa -N '' -f $PRIVATE_KEY -C "$EMAIL_ID"
  chmod 700 $KEYS_PATH
  chmod 644 $PUBLIC_KEY
  chmod 600 $PRIVATE_KEY
  chown -R daemon:daemon $KEYS_PATH
fi

#ssh postgres@$PG_PRIMARY_SERVICE_NAME
#ssh-copy-id
# SSH

# seed with defaults included in the container image, this is the
# case when /pgconf is not specified

cp $CONFDIR/* /tmp

bash /opt/cpm/bin/replace_conf.sh $PG_PRIMARY_SERVICE_NAME $PG_REPLICA_SERVICE_NAME


if [ $DOCKER_DEBUG == "on" ]; then
	sleep 999999999
fi

# Populate pool_passwd file
pg_md5 --md5auth --username=$PG_USERNAME --config=$CONFIGS/pgpool.conf $PG_PASSWORD
pg_md5 --md5auth --username=postgres --config=$CONFIGS/pgpool.conf $POSTGRES_PASSWORD

# EXTERNAL
pg_md5 --md5auth --username=$PG_EXTERNAL_USER --config=$CONFIGS/pgpool.conf $PG_EXTERNAL_PASSWORD

# PCP without password
echo "$PG_USERNAME:$(pg_md5 $PG_PASSWORD)" > /etc/pgpool-II-96/pcp.conf
#export PCPPASSFILE=/tmp/.pcppass
echo "*:*:$PG_USERNAME:$PG_PASSWORD" > /tmp/.pcppass
chmod 0600 /tmp/.pcppass

# Start pgpool
PGPOOL_DUMMY="0"
while [ $PGPOOL_DUMMY == "0" ];
do
  echo "[START] Init pgpool....................................."
  pgpool -n -a $CONFIGS/pool_hba.conf -f $CONFIGS/pgpool.conf  >> /tmp/pgpool.log 2>&1 &
  sleep 10
  export PGPOOL_PID=$!
  while pgrep -F /tmp/pgpool.pid > /dev/null
  do
    sleep $TIME_FAILOVER
    if [ $AUTOFAILOVER == "on" ]; then
      if [ $FAILOVER_MODE == "on" ]; then
        #bash /opt/cpm/bin/failover.sh
        #bash /opt/cpm/bin/auto_failback.sh
        bash /opt/cpm/bin/others/postgres_ha.sh "pgpool_failover"
      else
        bash /opt/cpm/bin/others/postgres_ha.sh "pgpool_dummy"
      fi
    fi
    sleep 10
  done
  if [ $AUTOFAILOVER != "on" ] && [ $FAILOVER_MODE != "on" ]; then
    PGPOOL_DUMMY="1"
  fi
done

#pgpool -f /tmp/pgpool.conf  reload

echo "waiting for pgpool to be signaled..."
wait