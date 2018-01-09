
generate-dhparam:
	rm -rf files/liberty-ingress/dhparam.pem
	openssl dhparam -out files/liberty-ingress/dhparam.pem 4096

build:
	docker build -f Dockerfile -t tedezed/liberty-dynamic-ingress:latest .
	rm -rf files/liberty-ingress/certs/*
	rm -rf files/liberty-ingress/default-cert/*

push:
	docker push tedezed/liberty-dynamic-ingress:latest
