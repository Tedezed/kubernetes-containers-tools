# Chronos

<!---
## Universal backup and snapshot system

Chronos is based on old Slug backup with the improvement of being modular and the possibility of working outside of Kubernetes.

Image `tedezed/chronos`

Database modules:
- [x] PostgreSQL
- [x] MySQL
- [ ] MariaDB
- [ ] Oracle
- [ ] SQLite
- [ ] Microsoft SQL Server
- [ ] MongoDB
- [ ] Cassandra
- [ ] Redis
- [ ] CouchDB
- [ ] Firebase
- [ ] YugabyteDB

Cloud disk support:
- [x] GCP compute disk
- [ ] AWS
- [ ] Azure
- [ ] Openstack Cinder
- [ ] Kubevirt disk

Other backup:
- [ ] Application backup path
- [ ] Kubernetes, API conf IN json of cluster

Other functionalities:
- [ ] Encryption of backups on disk
- [ ] Rrestore and test every dump

kubectl cp $HOME/git/kubernetes-containers-tools/chronos/docker/chronos kube-system/$(kgpod chronos):/
-->

Working Modes:
- databases
- disks

Conf modes:
- api
- configmap