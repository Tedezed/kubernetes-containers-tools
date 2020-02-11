kubectl create namespace sawtooth

for i in $(seq 0 1 3); do 

gcloud compute disks create sawtooth-$i --size=5GB --zone=europe-west1-b
cat <<EOF | kubectl apply -f -
apiVersion: v1

kind: List

items:

- apiVersion: v1
  kind: PersistentVolume
  metadata:
    name: sawtooth-$i
    namespace: sawtooth
  spec:
    accessModes:
    - ReadWriteMany
    capacity:
      storage: 5Gi
    gcePersistentDisk:
      fsType: ext4
      pdName: sawtooth-$i
      readOnly: false
    claimRef:
      name: sawtooth-$i
      namespace: sawtooth

- apiVersion: v1
  kind: PersistentVolumeClaim
  metadata:
    name: sawtooth-$i
    namespace: sawtooth
  spec:
    accessModes:
    - ReadWriteMany 
    resources:
       requests:
         storage: 5Gi

- apiVersion: extensions/v1beta1
  kind: Deployment
  metadata:
    name: sawtooth-$i
    namespace: sawtooth
  spec:
    replicas: 1
    template:
      metadata:
        labels:
          app: sawtooth
          node: sawtooth-$i
      spec:
        containers:
          - name: sawtooth-devmode-engine
            image: hyperledger/sawtooth-devmode-engine-rust:1.1
            command:
              - bash
            args:
              - -c
              - "devmode-engine-rust -C tcp://\$HOSTNAME:5050"

          - name: sawtooth-settings-tp
            image: hyperledger/sawtooth-settings-tp:1.1
            command:
              - bash
            args:
              - -c
              - "settings-tp -vv -C tcp://\$HOSTNAME:4004"

          - name: sawtooth-intkey-tp-python
            image: hyperledger/sawtooth-intkey-tp-python:1.1
            command:
              - bash
            args:
              - -c
              - "intkey-tp-python -vv -C tcp://\$HOSTNAME:4004"

          - name: sawtooth-xo-tp-python
            image: hyperledger/sawtooth-xo-tp-python:1.1
            command:
              - bash
            args:
              - -c
              - "xo-tp-python -vv -C tcp://\$HOSTNAME:4004"

          - name: sawtooth-validator
            image: hyperledger/sawtooth-validator:1.1
            env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            ports:
              - name: tp
                containerPort: 4004
              - name: consensus
                containerPort: 5050
              - name: validators
                containerPort: 8800
            command:
              - bash
            args:
              - -c
              - "mkdir -p /etc/sawtooth/keys && \
              if [ ! -e /etc/sawtooth/keys/validator.priv ]; then \
                  sawadm keygen; \
              fi && \
              if [ ! -e /root/.sawtooth/keys/key.priv ]; then \
                  sawtooth keygen key; \
              fi && \
              if [ ! -e /etc/sawtooth/config-genesis.batch ]; then \
                sawset genesis -k /root/.sawtooth/keys/key.priv -o /etc/sawtooth/config-genesis.batch; \
              fi && \  
              if [ ! -e /etc/sawtooth/config.batch ]; then \
                  echo '[INFO] Create config.batch'; \
                  sawset proposal create \
                    -k /root/.sawtooth/keys/key.priv \
                    sawtooth.consensus.algorithm.name=Devmode \
                    sawtooth.consensus.algorithm.version=0.1 \
                    -o /etc/sawtooth/config.batch; \
              fi && \
              if [ ! -e /var/lib/sawtooth/genesis.batch ] && [ ! -e /var/lib/sawtooth/block-00.lmdb ]; then \
                  echo '[INFO] Create genesis.batch'; \
                  sawadm genesis /etc/sawtooth/config-genesis.batch /etc/sawtooth/config.batch; \
              fi \
              && sawtooth-validator -vv \
                  --endpoint tcp://\$SAWTOOTH_0_SERVICE_HOST:8800 \
                  --bind component:tcp://eth0:4004 \
                  --bind consensus:tcp://eth0:5050 \
                  --bind network:tcp://eth0:8800 \
                  --seeds tcp://sawtooth-0:8800 \
                  --seeds tcp://sawtooth-1:8800 \
                  --seeds tcp://sawtooth-2:8800 \
                  --seeds tcp://sawtooth-3:8800"
            volumeMounts:
            - name: sawtooth-data
              mountPath: "/var/lib/sawtooth"
              subPathExpr: lib
            - name: sawtooth-data
              mountPath: "/root/.sawtooth"
              subPathExpr: userkeys
            - name: sawtooth-data
              mountPath: "/etc/sawtooth"
              subPathExpr: etc

          - name: sawtooth-rest-api
            image: hyperledger/sawtooth-rest-api:1.1
            ports:
              - name: api
                containerPort: 8008
            command:
              - bash
            args:
              - -c
              - "sawtooth-rest-api -C tcp://\$HOSTNAME:4004"

          - name: sawtooth-shell
            image: hyperledger/sawtooth-shell:1.1
            command:
              - bash
            args:
              - -c
              - "sawtooth keygen && tail -f /dev/null"
        volumes:
        - name: sawtooth-data
          persistentVolumeClaim:
            claimName: sawtooth-$i

- apiVersion: v1
  kind: Service
  metadata:
    name: sawtooth-$i
    namespace: sawtooth
  spec:
    type: ClusterIP
    selector:
      node: sawtooth-$i
    ports:
      - name: "4004"
        protocol: TCP
        port: 4004
        targetPort: 4004
      - name: "5050"
        protocol: TCP
        port: 5050
        targetPort: 5050
      - name: "8008"
        protocol: TCP
        port: 8008
        targetPort: 8008
      - name: "8800"
        protocol: TCP
        port: 8800
        targetPort: 8800
EOF

done



cat <<EOF | kubectl apply -f -
apiVersion: v1

kind: List

items:

- apiVersion: v1
  kind: Service
  metadata:
    name: sawtooth
    namespace: sawtooth
  spec:
    type: ClusterIP
    selector:
      app: sawtooth
    ports:
      - name: "4004"
        protocol: TCP
        port: 4004
        targetPort: 4004
      - name: "5050"
        protocol: TCP
        port: 5050
        targetPort: 5050
      - name: "8008"
        protocol: TCP
        port: 8008
        targetPort: 8008
      - name: "8800"
        protocol: TCP
        port: 8800
        targetPort: 8800
EOF