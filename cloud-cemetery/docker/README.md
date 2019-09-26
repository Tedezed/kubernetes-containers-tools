# Cloud Cemetery

Docker cron to schedule final resource deletions.

Create secret with credentials
```
cat <<EOF | kubectl create -f -
apiVersion: v1
kind: Secret
metadata:
  name: cloud-cementery
  namespace: kube-system
data:
  $(cat /XXXXXX/gcloud-project1.json | jq .project_id | tr -d '"'): $(cat /XXXXXX/gcloud-project1.json | base64 -w0)
  $(cat /XXXXXX/gcloud-project2.json | jq .project_id | tr -d '"'): $(cat /XXXXXX/gcloud-project2.json | base64 -w0)
  $(cat /XXXXXX/gcloud-project3.json | jq .project_id | tr -d '"'): $(cat /XXXXXX/gcloud-project3.json | base64 -w0)
  $(cat /XXXXXX/gcloud-project4.json | jq .project_id | tr -d '"'): $(cat /XXXXXX/gcloud-project4.json | base64 -w0)
EOF
```