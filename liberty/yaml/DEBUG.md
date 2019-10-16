## Helm Elastic Stack

cd charts/stable/elastic-stack
helm dependency update

helm install --name=elastic-stack-minimal --namespace=elastic-stack \
	--set elasticsearch.enabled=true \
	--set elasticsearch.client.replicas=1 \
	--set elasticsearch.master.replicas=3 \
	--set elasticsearch.data.replicas=1 \
	--set logstash.enabled=true \
	--set kibana.enabled=false \
	--set filebeat.enabled=false \
	--set fluentd.enabled=false \
	--set fluent-bit.enabled=false \
	--set fluentd-elasticsearch.enabled=false \
	--set nginx-ldapauth-proxy.enabled=false \
	--set elasticsearch-curator.enabled=false \
	--set elasticsearch-exporter.enabled=false \
	--dry-run --debug .

helm install --name=elastic-stack --namespace=elastic-stack \
	--set elasticsearch.enabled=true \
	--set elasticsearch.client.replicas=1 \
	--set elasticsearch.master.replicas=3 \
	--set elasticsearch.data.replicas=1 \
	--set logstash.enabled=true \
	--set logstash.elasticsearch.host=elasticsearch-client.elastic-stack.svc.cluster.local \
	--set kibana.enabled=false \
	--set filebeat.enabled=false \
	--set fluentd.enabled=false \
	--set fluent-bit.enabled=false \
	--set fluentd-elasticsearch.enabled=false \
	--set nginx-ldapauth-proxy.enabled=false \
	--set elasticsearch-curator.enabled=false \
	--set elasticsearch-exporter.enabled=false \
	.

helm install --name=elastic-stack --namespace=elastic-stack \
	--set elasticsearch.client.replicas=1 \
	--set elasticsearch.master.replicas=3 \
	--set elasticsearch.data.replicas=1 \
	--set logstash.elasticsearch.host=elastic-stack-elasticsearch-client.elastic-stack.svc.cluster.local \
	.


Configure Filebeat to send logs to logstash
watch kubectl get pod -n elastic-stack

helm list
helm delete --purge elastic-stack

## Helm Elastic Minimal

cd charts/stable/elasticsearch
helm install --name=elasticsearch-minimal --namespace=elasticsearch-minimal \
	--set client.replicas=1 \
	--set master.replicas=3 \
	--set data.replicas=1 \
	--dry-run --debug .
helm install --name=elasticsearch-minimal --namespace=elasticsearch-minimal \
	--set client.replicas=1 \
	--set master.replicas=3 \
	--set data.replicas=1 \
	.

Configure Filebeat to send logs to elasticsearch

helm delete --purge elasticsearch-minimal


## Filebeat for Liberty

vi /etc/filebeat.yml

filebeat.inputs:
- type: log
  paths:
    - /var/log/nginx/access.log
    - /var/log/nginx/custom_error.log
  input_type: log
  json.keys_under_root: true
  json.add_error_key: true
  json.message_key: log

output.logstash:
  hosts: ["elastic-stack-logstash.elastic-stack.svc.cluster.local:5044"]


## Test

kubectl port-forward svc/elastic-stack-elasticsearch-client -n elastic-stack 9200:9200

Get indeces: `curl -X GET "localhost:9200/_cat/indices?v&pretty"`

Get content under index: `curl -H 'Content-Type: application/json' -X GET https://localhost:9200/filebeat-2019.10.14/_search?pretty`

---

export ELK='true'
export ELK_LIBERTY_NAMES='liberty'
export ELK_MODE='start'
export ELK_HOST='elastic-stack-elasticsearch-client.elastic-stack.svc.cluster.local'

python /files/liberty-ingress/main.py