# Elastic

## Documentation

List indices
```
curl 'localhost:9200/_cat/indices?format=json&pretty=true'
```

List snapshot
```
curl 'localhost:9200/_snapshot/_all?format=json&pretty=true'
```

## Elasticsearch dump

Repository: https://github.com/elasticsearch-dump/elasticsearch-dump.git
Commit elasticsearch-dump: `6e05e4189dd4b4686ad8fe853caea51e2e932519`

Install:
```
curl -sL https://deb.nodesource.com/setup_10.x | bash -
sudo apt-get install -y nodejs
sudo npm install elasticdump -g

#Types: data, settings, analyzer, mapping, alias

elasticdump \
  --input=http://localhost:9200/filebeat-2020.10.28 \
  --type=data \
  --output=$ \
  | gzip > filebeat-2020.10.28-data.json.gz

elasticdump \
  --input=http://localhost:9200/filebeat-2020.10.28 \
  --type=mapping \
  --output=$ \
  | gzip > filebeat-2020.10.28-mapping.json.gz

elasticdump \
  --input=http://localhost:9200/filebeat-2020.10.28 \
  --type=data \
  --fileSize=1024mb \
  --output=data.json
```