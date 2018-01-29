# Slug Containers Tools <img src="https://raw.githubusercontent.com/tedezed/slug-containers/master/docs/img/slug.png" width="100">

## [Slug StatefulSet autoscaler](https://github.com/Tedezed/slug-containers/tree/master/statefulset_autoscaler)

Image `tedezed/slug-statefulset-autoscaler:latest`

- [x] Docker build
- [x] Docker image in Docker Hub
- [x] Autoscaler StatefulSet
- [x] Autoscaler using CPU
- [x] Autoscaler using max/min replicas
- [x] Autoreduce StatefulSet Normal (Simple containers)
- [ ] Autoscaler StatefulSet crunchy-containers
- [ ] Autoreduce StatefulSet crunchy-containers

Example of usage: http://www.aventurabinaria.es/kubernetes-stateful-set-autoscale/

## [Slug backup/snapshot ](https://github.com/Tedezed/slug-containers/tree/master/backup-db-cron)

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

## [Slug emailing ](https://github.com/Tedezed/slug-containers/tree/master/emailing)

Solution to send emails in the cloud

Image `tedezed/emailing`

- [x] Docker build
- [x] Docker image in Docker Hub
- [x] Test with Mailjet
- [x] Test in GCP
- [ ] Test in AWS

## [Slug phpBB](https://github.com/Tedezed/slug-containers/tree/master/phpbb)

Personal image for mount phpBB

Image `tedezed/slug-phpbb`

- [x] Docker build
- [x] Docker image in Docker Hub
- [x] Language EN
- [x] Language ES

## [SFTP Multiuser](https://github.com/Tedezed/slug-containers/tree/master/sftp-share)

SFTP for multiple users

Image `tedezed/sftpd-multiuser`

- [x] Docker build
- [x] Docker image in Docker Hub
- [x] Modes: one user, list users.
- [ ] Security improvements.
- [ ] Read permissions.

## [Slug StatefulSet load balancer](https://github.com/Tedezed/slug-containers/tree/master/dynamic_loadbalancer)

Dynamic load balancer for StatefulSet autoscaler "Test"

Image `tedezed/slug-statefulset-dynamic-loadbalancer`

- [x] Docker build
- [x] Docker image in Docker Hub
- [x] Dynamic load balancer, using number of replicas of StatefulSet
- [x] Support replication controller.
- [ ] Load balancing for all StatefulSet with labels: `slug_loadbalancing: "true"`
