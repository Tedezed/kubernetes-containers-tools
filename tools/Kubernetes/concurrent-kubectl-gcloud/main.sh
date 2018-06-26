#!/bin/bash

# Easy concurrent kubectl Multi-Project/Multi-Cluster for GCP without switch
# 
# https://github.com/kubernetes/kubernetes/issues/44476
# Use: 
#	kubectl --kubeconfig ~/.kube/config_nagios --context=gke_proy-20_zone-xxxxx_cluster-1 get pod --all-namespaces
#	kubectl --kubeconfig ~/.kube/config_nagios --context=gke_proy-26_zone-xxxxx_cluster-8 get pod --all-namespaces

# Load and generate array of token for users Kubernetes
json_users="["
for f in sa/*.json; do
	sa_json=$(cat $f)
	gcloud auth activate-service-account --key-file=$f
	gcloud config set project $(echo $sa_json | jq -r '.project_id')
	gcloud config set compute/zone $(echo $sa_json | jq -r '.zone')
	gcloud config set container/cluster $(echo $sa_json | jq -r '.project_id')
	gcloud container clusters get-credentials $(echo $sa_json | jq -r '.cluster')
	if [ "$json_users" != "[" ]; then
		json_users="$json_users, "
	fi
	# Example {"name": "gke_proy-xxxxx_zone-xxxxx_cluster-xxx","user": {"token": "token.xxxxx"}}
	json_users="$json_users{\"name\": \"gke_$(echo $sa_json | jq -r '.project_id')_$(echo $sa_json | jq -r '.zone')_$(echo $sa_json | jq -r '.cluster')\",\"user\": {\"token\": \"$(gcloud auth print-access-token --account=$(echo $sa_json | jq -r '.client_email'))\"}}"
done
json_users="$json_users]"
echo $json_users > $HOME/.kube/json_users.json

# YAML to JSON
cp $HOME/.kube/config $HOME/.kube/config_nagios
ruby -ryaml -rjson -e 'puts JSON.pretty_generate(YAML.load(ARGF))' < $HOME/.kube/config_nagios > $HOME/.kube/config_nagios.json

# Delete users on json
jshon -d "users" < $HOME/.kube/config_nagios.json > $HOME/.kube/config_nagios.json.tmp
mv $HOME/.kube/config_nagios.json.tmp $HOME/.kube/config.json

# Add users to json whith empty content
jshon -s "" -i users < $HOME/.kube/config_nagios.json > config_nagios.json.tmp

# Add token for the users
ruby -rjson -e 'j=JSON.parse(File.read("config_nagios.json.tmp")); j["users"]=JSON.load(ARGF); puts JSON.dump(j)' < $HOME/.kube/json_users.json > $HOME/.kube/config_nagios.json.tmp
mv $HOME/.kube/config_nagios.json.tmp $HOME/.kube/config_nagios.json
rm config_nagios.json.tmp

# JSON to YAML
ruby -ryaml -rjson -e 'puts YAML.dump(JSON.load(ARGF))' < $HOME/.kube/config_nagios.json > $HOME/.kube/config_nagios
cat $HOME/.kube/config_nagios
