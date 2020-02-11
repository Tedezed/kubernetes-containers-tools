kubectl delete namespace sawtooth

gcloud compute disks delete sawtooth-0 --zone=europe-west1-b \
&& gcloud compute disks delete sawtooth-1 --zone=europe-west1-b \
&& gcloud compute disks delete sawtooth-2 --zone=europe-west1-b \
&& gcloud compute disks delete sawtooth-3 --zone=europe-west1-b

kubectl delete pv sawtooth-0 \
&& kubectl delete pv sawtooth-1 \
&& kubectl delete pv sawtooth-2 \
&& kubectl delete pv sawtooth-3
