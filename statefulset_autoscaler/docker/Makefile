debug:
	cp ~/.kube/config ~/.kube/config-slug
	sed -i -E "s#server: https://.*#server: https://kubernetes#" ~/.kube/config-slug
	python slug_statefulset_autoscaler/main.py url_heapster=http://heapster/api/v1/model autoscaler_count=2 time_query=18
