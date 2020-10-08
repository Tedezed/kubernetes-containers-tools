# By: Juan Manuel Torres
# GitHub: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

build:
	docker build -f Dockerfile -t tedezed/chronos:latest .

push:
	docker push tedezed/chronos:latest

push-debug:
	docker tag tedezed/chronos:latest tedezed/chronos:debug
	docker push tedezed/chronos:debug
