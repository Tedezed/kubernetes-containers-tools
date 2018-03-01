# Test dynamic load balancer for StatefulSet

Image `tedezed/slug-statefulset-dynamic-loadbalancer`

- [x] Docker build
- [x] Docker image in Docker Hub
- [x] Dynamic load balancer, using number of replicas of StatefulSet
- [x] Support replication controller.
- [ ] Load balancing for all StatefulSet with labels: `slug_loadbalancing: "true"`