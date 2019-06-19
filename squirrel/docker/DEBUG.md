kubectl create sa squirrel -n default
kubectl create clusterrolebinding squirrel-admin-binding -n default \
    --clusterrole cluster-admin \
    --serviceaccount default:squirrel

cat <<EOF | kubectl create -f -
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  labels:
    run: squirrel
  name: squirrel
  namespace: default
spec:
  selector:
    matchLabels:
      run: squirrel
  template:
    metadata:
      labels:
        run: squirrel
    spec:
      serviceAccountName: squirrel
      containers:
      - image: tedezed/squirrel
        imagePullPolicy: Always
        name: squirrel
EOF

make build && make push && kubectl delete pod $(kubectl get pod | grep squirrel | awk '{ print $1 }')
kubectl exec -it $(kubectl get pod | grep squirrel | awk '{ print $1 }') bash

./main.py mode="client-create-key" key_file="local.key" email="juanmanuel.torres@aventurabinaria.es"

cat <<EOF | kubectl create -f -
apiVersion: "tree.squirrel.local/v1"
kind: Nutcrackers
metadata:
  name: juanmanuel.torres
type: Opaque
data:
  email: "juanmanuel.torres@aventurabinaria.es"
  keypub: $(cat local.key.pub | base64 -w0)
EOF