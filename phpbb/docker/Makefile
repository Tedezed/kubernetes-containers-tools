build:
	docker build -f Dockerfile -t tedezed/slug-phpbb:latest .

run:
	docker run -d -p 8080:80 tedezed/slug-phpbb:latest

drop:
	sh ../../tools/docker/drop-docker.sh

push:
	docker push tedezed/slug-phpbb:latest

run-debug:
	docker run -p 8080:80 tedezed/slug-phpbb:latest
