
generate-dhparam:
	rm -rf files/liberty-ingress/dhparam.pem
	openssl dhparam -out files/liberty-ingress/dhparam.pem 1024

build: generate-dhparam build-only

build-only:
	docker build -f Dockerfile -t tedezed/liberty-dynamic-ingress:latest .
	rm -rf files/liberty-ingress/certs/*
	rm -rf files/liberty-ingress/default-cert/*

push:
	docker push tedezed/liberty-dynamic-ingress:latest

debug:
	echo "......."
	echo "Copy: cp ~/.kube/config ~/.kube/config-slug"
	echo "Replace: - cluster -> sever:'https://IP' in ~/.kube/config-slug to 'https://kuberentes' and add IP kuberentes to /etc/hosts"
	echo "......."
	python files/liberty-ingress/main.py