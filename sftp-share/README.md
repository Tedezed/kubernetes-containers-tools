# SFTPD Docker

Source [luzifer/sftp-share](https://hub.docker.com/r/luzifer/sftp-share/)

## Base Docker Image

- [ubuntu](https://registry.hub.docker.com/_/ubuntu/)

## Modes

### Mode only one user

```
apiVersion: v1
kind: Service
metadata:
  name: sftp-server
  labels:
    app: sftp-server
spec:
  #type: NodePort
  type: LoadBalancer
  ports:
    - port: 22
      protocol: TCP
  selector:
    app: sftp-server
---
apiVersion: v1
kind: ReplicationController
metadata:
  name: sftp-server
  labels:
    app: sftp-server
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: sftp-server
    spec:
      containers:
      - name: sftp-server
        image: tedezed/sftpd-multiuser:latest
        env:
          - name: MODE
            value: "one_user"
          - name: OWNER
            value: "www-data"
          - name: USER
            value: "ted"
          - name: PASS
            value: "tedpass"
          - name: DIR
            value: "/data/demo"
        ports:
        - containerPort: 22
        volumeMounts:
        - name: persistent-storage
          mountPath: /data/demo
      volumes:
        - name: persistent-storage
          persistentVolumeClaim:
            claimName: demo
```


### Mode only one user with gcsfuse

Credentials storage:

```
kubectl create secret generic storage-credentials \
    --from-file=credentials.json=/home/ted/key-12345.json  \
    -n default
```

Deployment:

```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  labels:
    app: test-bucket
  name: test-bucket
  namespace: default
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: test-bucket
    spec:
      containers:
      - name: sftp-server
        image: tedezed/sftpd-multiuser:latest
        env:
          - name: MODE
            value: "gcsfuse"
          - name: SHELL
            value: "/bin/sh"
          - name: OWNER
            value: "www-data"
          - name: OWNER_UID
            value: "33"
          - name: USER
            value: "ted"
          - name: PASS
            value: "tedpass"
          - name: DIR
            value: "/data/content"
          - name: BUCKET_NAME
            value: "test-storage"
          - name: GOOGLE_APPLICATION_CREDENTIALS
            value: "/secrets/cloud/credentials.json"
        ports:
        - containerPort: 22
        securityContext:
          privileged: true
          capabilities:
            add:
              - SYS_ADMIN
        lifecycle:
          preStop:
            exec:
              command: ["fusermount", "-zu", "/data/content"]
        volumeMounts:
            - name: storage-credentials
              mountPath: /secrets/cloud
              readOnly: false
      volumes:
        - name: storage-credentials
          secret:
            secretName: storage-credentials
```


### Mode List user 

(Do not use this method, need security improvements):

```
apiVersion: v1
kind: Service
metadata:
  name: sftp-server
  labels:
    app: sftp-server
spec:
  #type: NodePort
  type: LoadBalancer
  ports:
    - port: 22
      protocol: TCP
  selector:
    app: sftp-server
---
apiVersion: v1
kind: ReplicationController
metadata:
  name: sftp-server
  labels:
    app: sftp-server
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: sftp-server
    spec:
      containers:
      - name: sftp-server
        image: tedezed/sftpd-multiuser:latest
        env:
          - name: MODE
            value: "user_list"
          - name: LIST_USERS
            value: "admin:admin:www-data:/data ted:ted2:www-data:/data/demo"
        ports:
        - containerPort: 22
        volumeMounts:
        - name: persistent-storage
          mountPath: /data/demo
      volumes:
        - name: persistent-storage
          persistentVolumeClaim:
            claimName: demo
```
