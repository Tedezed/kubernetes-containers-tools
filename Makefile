slug-backup-cron:
	cd backup-db-cron/docker && docker build -f Dockerfile -t tedezed/slug-backup-db-cron:latest .
	docker push tedezed/slug-backup-db-cron:latest

slug-dynamic_loadbalancer:
	cd dynamic_loadbalancer/docker && docker build -f Dockerfile -t tedezed/slug-dynamic-loadbalancer:latest .
	docker push tedezed/slug-dynamic-loadbalancer:latest

slug-statefulset_autoscaler:
	cd statefulset_autoscaler/docker && docker build -f Dockerfile -t tedezed/slug-statefulset-autoscaler:latest .
	docker push tedezed/slug-statefulset-autoscaler:latest
	kubectl patch deployment slug-autoscaler -p "{\"spec\":{\"template\":{\"metadata\":{\"labels\":{\"date\":\"`date +'%s'`\"}}}}}" -n kube-system
