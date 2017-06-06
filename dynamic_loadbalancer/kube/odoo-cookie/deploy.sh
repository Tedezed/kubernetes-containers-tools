kubectl delete -f odoo-pg-vol.yaml
kubectl delete -f slug-loadbalancer.yaml

sleep 4

gcloud compute disks delete disk-test-pg disk-test-odoo

gcloud compute disks create --size 15GB disk-test-pg
gcloud compute disks create --size 15GB disk-test-odoo

kubectl create -f odoo-pg-vol.yaml
kubectl create -f slug-loadbalancer.yaml