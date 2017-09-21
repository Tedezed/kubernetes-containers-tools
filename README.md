# Slug Containers Tools

<img src="https://raw.githubusercontent.com/tedezed/slug-containers/master/docs/img/slug.png" width="100">

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

## [Slug backup for all databases using cron of Kubernetes](https://github.com/Tedezed/slug-containers/tree/master/backup-db-cron)

Image `tedezed/slug-backup-db-cron`

- [x] Docker build
- [x] Docker image in Docker Hub
- [x] Support PostgreSQL
- [ ] Support MySQL
- [ ] Support MongoDB
- [ ] Support Oracle
- [x] Date for drop
- [ ] Auto backup rotation

## [Slug dynamic load balancer for StatefulSet autoscaler "Test"](https://github.com/Tedezed/slug-containers/tree/master/dynamic_loadbalancer)

Image `tedezed/slug-statefulset-dynamic-loadbalancer`

- [x] Docker build
- [x] Docker image in Docker Hub
- [x] Dynamic load balancer, using number of replicas of StatefulSet
- [x] Support replication controller.
- [ ] Load balancing for all StatefulSet with labels: `slug_loadbalancing: "true"`