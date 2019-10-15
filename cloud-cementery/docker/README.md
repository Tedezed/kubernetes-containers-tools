# Cloud Cementery

Docker delete resources with delay on a scheduled basis.

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

Create cronjob Kubernetes
```
kubectl create -f ../kube/cronjob.yaml
```

# Send disks or snapshots to cementery

This command create a snapshot and delete your disks. In the new snaposhot will add one label with `funeral-home=true` or `cementery=true`, this label and date of creation, is use with the cron to delete snapshot in the future.
The advantages of passing a disk to snapshot are: reduced cost, it only occupies the space used.

Add in your `.bash_profile`
```
function gcloud_cold_disk () {
	# gcloud compute disks snapshot disk-test --zone europe-west1-b --snapshot-names snapshot-disk-test --storage-location=europe-west1
	gcloud compute disks snapshot $1 --zone $2 --snapshot-names cold-$1 --storage-location=$3
	gcloud compute disks delete $1 --zone $2
}

function gcloud_kill_disk () {
	# gcloud compute disks snapshot disk-test --zone europe-west1-b --snapshot-names snapshot-disk-test --storage-location=europe-west1
	gcloud compute disks snapshot $1 --zone $2 --snapshot-names dead-$1 --storage-location=$3 --labels funeral-home=true
	gcloud compute disks delete $1 --zone $2
}
```

Execute in your disk:
```
gcloud_kill_disk NAME_DISK ZONE REGION
```