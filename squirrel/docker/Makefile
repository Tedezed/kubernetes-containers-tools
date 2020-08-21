# Creator: Juan Manuel Torres
# GitHub: https://github.com/Tedezed
# Mail: juanmanuel.torres@aventurabinaria.es

build:
	#rm -rf squirrel/*.key
	#rm -rf squirrel/*.pub
	docker build -f Dockerfile -t tedezed/squirrel:latest .

push:
	docker push tedezed/squirrel:latest

push-debug:
	docker tag tedezed/squirrel:latest tedezed/squirrel:debug
	docker push tedezed/squirrel:debug
