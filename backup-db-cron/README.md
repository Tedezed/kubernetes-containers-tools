# Slug backup

## Sug backup/snapshot

Slug backup for all databases and snapshot for all disks using cron of Kubernetes

Image `tedezed/slug-backup-db-cron`

- [x] Docker build
- [x] Docker image in Docker Hub
- [x] Support PostgreSQL
- [x] Support MySQL
- [ ] Support MariaDB
- [ ] Support MongoDB
- [ ] Support Oracle
- [x] Date for drop
- [x] Auto backup rotation
- [x] Support snapshot GCP
- [ ] Support snapshot AWS

### Description:

Path of the backups: `/slug-backup-db-cron/backups`

#### Docker variables

* **MODE**:
  * `1`: Backup
  * `2`: Snapshot
  * `3`: Backup + Snapshot
* **CONF_MODE**
  * `secret`: Configuration in file on secrets.
  * `conf-map`: Configuration in ConfigMap.
* **PROJECT**: Proyect of Google Cloud.
* **ZONE**: Zone of the disk in Google CLoud.
* **TIME**: Time in format for crontab.
* **DAYS_TO_DROP**
* **DAYS_TO_DROP_SNAPSHOT**
* **EMAIL_MODE**: Sending alertsm, use OFF or SMTP.
* **EMAIL_SEND_TO**
* **EMAIL_SERVER**
* **EMAIL_PORT**
* **EMAIL_USER**
* **EMAIL_PASSWORD**


### Configuration modes:

#### CONF_MODE: `secret`

Configure secrets:

`nano kube-backup-cron-configmap.yaml`

```
backup-db-cron: v1
data:
  service-name1: |
    POSTGRES_USER=root
    POSTGRES_PASSWORD=rootpass
    namespace=default
    type=postgres
    port=5432
  service-name2: |
    POSTGRES_USER=root
    POSTGRES_PASSWORD=rootpass
    namespace=production
    type=postgres
    port=2345
```

`nano kube-snapshot-cron-configmap.yam`

```
backup-db-cron: v1
data:
  disk-test1: |
    zone=europe-west1-b
  disk-test2: |
    zone=europe-west1-b
```

Create secrets:
```
kubectl create secret generic backup-conf --from-file=kube-backup-cron-configmap.yaml=kube-backup-cron-configmap.yaml -n kube-system
kubectl create secret generic snapshot-conf --from-file=kube-snapshot-cron-configmap.yaml=kube-snapshot-cron-configmap.yam -n kube-system
```

Create container:

```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: slug-backup-database
  namespace: kube-system
---
apiVersion: v1
kind: ReplicationController
metadata:
  name: slug-backup-database
  namespace: kube-system
  labels:
    app: slug-backup-database
spec:
  replicas: 1
  selector:
    name: slug-backup-database
  template:
    metadata:
      labels:
        name: slug-backup-database
    spec:
      serviceAccountName: slug-backup-database
      containers:
      - name: slug-backup-database
        image: tedezed/slug-backup-db-cron:latest
        env:
        - name: DAYS_TO_DROP
          value: "15"
        - name: DAYS_TO_DROP_SNAPSHOT
          value: "5"
        - name: TIME
          value: "10 3 * * *"
        - name: MODE
          value: "3"
        - name: PROJECT
          value: "name-pro"
        - name: ZONE
          value: "europe-west1-b"
        - name: CONF_MODE
          value: "secret"
        volumeMounts:
        - mountPath: /slug-backup-db-cron/backups
          name: vol-slug-backup-db-cron
          subPath: slug-backup-db-cron
        # Secrets
        - name: backup-conf
          mountPath: /secrets/backup
          readOnly: false
        - name: snapshot-conf
          mountPath: /secrets/snapshot
          readOnly: false
      volumes:
      - name: vol-slug-backup-db-cron
        persistentVolumeClaim:
          claimName: pvc-backups
      # Secrets
      - name: backup-conf
        secret:
          secretName: backup-conf
      - name: snapshot-conf
        secret:
          secretName: snapshot-conf
```

#### CONF_MODE: `conf-map`

Create ConfigMap:

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: kube-backup-cron-configmap
  namespace: kube-system
data:
  # Split database_list &
  service-name1: |
    mode=secret
    POSTGRES_USER=root
    POSTGRES_PASSWORD=rootpass
    namespace=default
    type=postgres
    port=5432
  service-name2: |
    POSTGRES_USER=pguser
    POSTGRES_PASSWORD=pgpass
    namespace=production
    type=postgres
    port=2345
```

Create container:

```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: slug-backup
  namespace: kube-system
---
apiVersion: v1
kind: ReplicationController
metadata:
  name: slug-backup
  namespace: kube-system
  labels:
    app: slug-backup
spec:
  replicas: 1
  selector:
    name: slug-backup
  template:
    metadata:
      labels:
        name: slug-backup
    spec:
      serviceAccountName: slug-backup
      containers:
      - name: slug-backup
        image: tedezed/slug-backup-db-cron
        env:
        - name: DAYS_TO_DROP
          value: "30"
        - name: DAYS_TO_DROP_SNAPSHOT
          value: "10"
        - name: TIME
          value: "10 12 * * *"
        - name: MODE
          value: "3"
        - name: PROJECT
          value: "pepperoni-xxxx"
        - name: ZONE
          value: "europe-xxxx"
        volumeMounts:
        - mountPath: /slug-backup-db-cron/backups
          name: vol-slug-backup
          subPath: slug-backup
      volumes:
      - name: vol-slug-backup
        persistentVolumeClaim:
          claimName: pvc-slug-backup
```

You can also use google disks and create snapshots with labels with MODE 4 or 5.
Cron: https://github.com/Tedezed/kubernetes-containers-tools/blob/master/backup-db-cron/docker/slug-backup-db-cron/start

Add label `backup`:
```
gcloud compute disks update disk-1 --update-labels backup=true
gcloud compute disks update disk-2 --update-labels backup=true
```

#### GCLOUD CUSTOM SA 

Custom role:
```
compute.disks.createSnapshot
compute.disks.get
compute.disks.list
compute.snapshots.create
compute.snapshots.delete
compute.snapshots.get
compute.snapshots.list
```

Variables:
```
GCLOUD_DEFAULT_CREDENTIALS="False"
GCLOUD_SA_FILE="/secrets/sa/sa-gcloud.json"
```

Create secret:
```
kubectl create secret generic backup-sa --from-file=sa-gcloud.json=xxxxxxxxxx.json -n kube-system
```

Edit your deploy:
```
  volumeMounts:
  - name: backup-sa
    mountPath: /secrets/sa/
volumes:
- name: backup-sa
  secret:
    secretName: backup-sa
```
