#!/bin/bash

PG_MASTER_REPLACE=$1
PG_REPLICA_REPLACE=$2

if [ $PGPOOL_MODE == "HA" ]; then
  cp /tmp/pgpool_ha.conf /tmp/pgpool.conf
elif [ $PGPOOL_MODE == "LOADBALANCING" ]; then
  cp /tmp/pgpool_loadbalancing.conf /tmp/pgpool.conf
fi

# populate template with env vars
sed -i "s/PG_PRIMARY_SERVICE_NAME/$PG_MASTER_REPLACE/g" $CONFIGS/pgpool.conf
sed -i "s/PG_REPLICA_SERVICE_NAME/$PG_REPLICA_REPLACE/g" $CONFIGS/pgpool.conf
sed -i "s/PG_USERNAME/$PG_USERNAME/g" $CONFIGS/pgpool.conf
sed -i "s/PG_PASSWORD/$PG_PASSWORD/g" $CONFIGS/pgpool.conf

# Personal configuration
sed -i "s/PG_NUM_INIT_CHILDREN/$PG_NUM_INIT_CHILDREN/g" $CONFIGS/pgpool.conf
sed -i "s/PG_MAX_POOL/$PG_MAX_POOL/g" $CONFIGS/pgpool.conf
sed -i "s/PG_MULTIPLER_BACK/$PG_MULTIPLER_BACK/g" $CONFIGS/pgpool.conf
sed -i "s/PG_CHILD_LIFE_TIME/$PG_CHILD_LIFE_TIME/g" $CONFIGS/pgpool.conf
sed -i "s/PG_CLIENT_IDLE_LIMIT/$PG_CLIENT_IDLE_LIMIT/g" $CONFIGS/pgpool.conf
sed -i "s/PG_MAX_CONNECTIONS/$PG_MAX_CONNECTIONS/g" $CONFIGS/pgpool.conf
sed -i "s/PG_SUPERUSER_RESERVED_CONNECTIONS/$PG_SUPERUSER_RESERVED_CONNECTIONS/g" $CONFIGS/pgpool.conf
sed -i "s#PG_DATA_DIRECTORY#$PG_DATA_DIRECTORY#g" $CONFIGS/pgpool.conf

#PCP
sed -i "s/PCP_PORT/$PCP_PORT/g" $CONFIGS/pgpool.conf

# Debug and log
sed -i "s/PG_DEBUG/$PG_DEBUG/g" $CONFIGS/pgpool.conf
sed -i "s/PG_LOG/$PG_LOG/g" $CONFIGS/pgpool.conf

if [ $FAILOVER_MODE == "on" ]; then
  FAILOVER_CONF="ALLOW_TO_FAILOVER"
else
  FAILOVER_CONF="DISALLOW_TO_FAILOVER"
fi
sed -i "s/FAILOVER_MODE/$FAILOVER_CONF/g" $CONFIGS/pgpool.conf
