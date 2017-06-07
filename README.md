# Slug StatefulSet autoscaler

Example of usage: http://www.aventurabinaria.es/kubernetes-stateful-set-autoscale/

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

## [Slug dynamic load balancer for StatefulSet autoscaler](https://github.com/Tedezed/slug-containers/tree/master/dynamic_loadbalancer)

Image `tedezed/slug-statefulset-dynamic-loadbalancer`

- [x] Docker build
- [x] Docker image in Docker Hub
- [x] Dynamic load balancer, using number of replicas of StatefulSet
- [x] Support replication controller.
- [ ] Load balancing for all StatefulSet with labels: `slug_loadbalancing: "true"`
