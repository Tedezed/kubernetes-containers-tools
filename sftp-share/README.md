# SFTPD Docker

Source [luzifer/sftp-share](https://hub.docker.com/r/luzifer/sftp-share/)

## Base Docker Image

- [ubuntu](https://registry.hub.docker.com/_/ubuntu/)

## Deploy

One user:

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

List user (Do not use this method, need security improvements):

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
