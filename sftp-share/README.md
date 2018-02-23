# SFTPD multiuser Docker

Project created to share with SFTP the volumes in the cloud.

A practical example is to access to volume for SFTP that uses a web aplication to be edited by an external client without access to the cluster of Kubernetes.

## Base Docker Image

- [ubuntu](https://registry.hub.docker.com/_/ubuntu/)
- Support buckets in GCP.

## Modes

* [Mode only one user](#mode-only-one-user)
* [Mode only one user with gcsfuse](#mode-only-one-user-with-gcsfuse)
* [Mode multiuser](#mode-multiuser)
* [Mode multiuser with gcsfuse](#mode-multiuser-with-gcsfuse)

## Mode only one user

Example Yaml:

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


Example with Wordpress:

```
apiVersion: v1
kind: ReplicationController
metadata:
  labels:
    app: wp-sftp
  name: wp-sftp
  namespace: ted-production
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: wp-sftp
    spec:
      containers:
      ####
      - name: wp-sftp
        image: wordpress:latest
        ports:
        - name: http
          containerPort: 80
        - name: https
          containerPort: 443
        env:
          - name: WORDPRESS_DB_HOST
            value: mysql-sftp
          - name: WORDPRESS_DB_USER
            value: wordpress
          - name: WORDPRESS_DB_PASSWORD
            value: wordpresspass
          - name: WORDPRESS_DB_NAME
            value: wordpress
        volumeMounts:
        - name: vol-wp-sftp
          mountPath: /var/www/html
          subPath: sftp/html
      ####
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
            value: "ted97pass"
          - name: DIR
            value: "/data/wp"
        ports:
        - containerPort: 22
        volumeMounts:
        - name: vol-wp-sftp
          mountPath: /data/wp
          subPath: sftp/html
      volumes:
      - name: vol-wp-sftp
        persistentVolumeClaim:
          claimName: wp-sftp
```

## Mode only one user with gcsfuse

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

You need `readOnly: false` on volumeMounts to change permission to 400 for the file /secrets/cloud/credentials.json, you can only read file if you are user root.

## Mode multiuser

Encrypt passwords for users:

```
$ openssl passwd -1 "adminpass"
$1$RDbfUWvO$HEJqJJ7248Xl8z5m8vLep1

$ openssl passwd -1 "ted97pass"
$1$pKDgLBpg$KBySprkP6NoMQRZfuZTnA/
```

File to generate the secret in Kubernetes: `nano sftp-multiuser-passwd`

```
admin:$1$RDbfUWvO$HEJqJJ7248Xl8z5m8vLep1:www-data:/data
ted:$1$pKDgLBpg$KBySprkP6NoMQRZfuZTnA/:www-data:/data/demo
```

Create secret:

```
kubectl create secret generic sftp-multiuser-db \
    --from-file=sftp-multiuser-db=sftp-multiuser-passwd \
    -n default
```

Example Yaml:

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
  namespace: default
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
          - name: SFTP_MULTIUSER_FILE
            value: "/secrets/sftp-multiuser/sftp-multiuser-db"
        ports:
        - containerPort: 22
        volumeMounts:
        - name: sftp-multiuser-db
          mountPath: /secrets/sftp-multiuser
          readOnly: false
        - name: persistent-storage
          mountPath: /data/demo
      volumes:
        - name: sftp-multiuser-db
          secret:
            secretName: sftp-multiuser-db
        - name: persistent-storage
          persistentVolumeClaim:
            claimName: demo
```

## Mode multiuser with gcsfuse

Encrypt passwords for users:

```
$ openssl passwd -1 "adminpass"
$1$RDbfUWvO$HEJqJJ7248Xl8z5m8vLep1

$ openssl passwd -1 "ted97pass"
$1$pKDgLBpg$KBySprkP6NoMQRZfuZTnA/
```

File to generate the secret in Kubernetes: `nano sftp-multiuser-passwd`

```
admin:$1$RDbfUWvO$HEJqJJ7248Xl8z5m8vLep1:www-data:/data/admin:name-bucket-admin
ted:$1$pKDgLBpg$KBySprkP6NoMQRZfuZTnA/:www-data:/data/ted:name-bucket-ted

```

Create secret:

```
kubectl create secret generic sftp-multiuser-db \
    --from-file=sftp-multiuser-db=sftp-multiuser-passwd \
    -n default
```

Credentials storage:

```
kubectl create secret generic storage-credentials \
    --from-file=credentials.json=/home/ted/key-12345.json  \
    -n default
```

Example Yaml:

```
apiVersion: v1
kind: Service
metadata:
  name: test-bucket
  namespace: default
  labels:
    app: test-bucket
spec:
  #type: NodePort
  type: LoadBalancer
  ports:
    - port: 22
      protocol: TCP
  selector:
    app: test-bucket
---
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
            value: "user_list_gcsfuse"
          - name: SFTP_MULTIUSER_FILE
            value: "/secrets/sftp-multiuser/sftp-multiuser-db"
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
              command: [
                "fusermount", "-zu", "/data/admin",
                "fusermount", "-zu", "/data/ted"
              ]
        volumeMounts:
            - name: sftp-multiuser-db
              mountPath: /secrets/sftp-multiuser
              readOnly: false
            - name: storage-credentials
              mountPath: /secrets/cloud
              readOnly: false
      volumes:
        - name: sftp-multiuser-db
          secret:
            secretName: sftp-multiuser-db
        - name: storage-credentials
          secret:
            secretName: storage-credentials
```

---

#### Credits

Based on [luzifer/sftp-share](https://hub.docker.com/r/luzifer/sftp-share/)