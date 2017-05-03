# Slug autoscaler

## [Slug StatefulSet Autoscaler](https://github.com/Tedezed/slug-containers/tree/master/statefulset_autoscaler)

Image `tedezed/slug-statefulset-autoscaler:latest`

- [x] Docker build
- [x] Docker image in Docker Hub
- [x] Autoscaler StatefulSet
- [x] Autoscaler using CPU
- [x] Autoscaler using max/min replicas
- [x] Autoreduce StatefulSet Normal (Simple containers)
- [ ] Autoscaler StatefulSet crunchy-containers
- [ ] Autoreduce StatefulSet crunchy-containers

## [Slug dynamic load balancer for StatefulSet Autoscaler](https://github.com/Tedezed/slug-containers/tree/master/statefulset_dynamic_loadbalancer)

- [ ] Docker build
- [ ] Docker image in Docker Hub
- [ ] Dynamic load balancer, using number of replicas of StatefulSet
- [ ] Load balancing for all StatefulSet with labels: `slug_loadbalancing: "true"`
