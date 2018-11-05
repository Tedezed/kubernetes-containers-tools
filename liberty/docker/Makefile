# Ingress Controller Liberty
# Creator: Juan Manuel Torres
# Source: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

build:
	docker build -f Dockerfile -t tedezed/liberty-dynamic-ingress:${VERSION_IMAGE} .
	rm -rf files/liberty-ingress/certs/*
	rm -rf files/liberty-ingress/default-cert/*

build-no-cache:
	bash tools/drop || true
	docker build -f Dockerfile -t tedezed/liberty-dynamic-ingress:${VERSION_IMAGE} --no-cache .
	rm -rf files/liberty-ingress/certs/*
	rm -rf files/liberty-ingress/default-cert/*

push:
	docker push tedezed/liberty-dynamic-ingress:${VERSION_IMAGE}

debug:
	echo "......."
	echo "Copy: cp ~/.kube/config ~/.kube/config-slug"
	echo "Replace: - cluster -> sever:'https://IP' in ~/.kube/config-slug to 'https://kuberentes' and add IP kuberentes to /etc/hosts"
	echo "......."
	python files/liberty-ingress/main.py
	#cat /etc/nginx/sites-enabled/default

force_pull_image:
	kubectl patch deployment liberty-ingress -p "{\"spec\":{\"template\":{\"metadata\":{\"labels\":{\"date\":\"`date +'%s'`\"}}}}}" -n kube-system

default: build push force_pull_image