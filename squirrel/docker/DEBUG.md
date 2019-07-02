kubectl create sa squirrel -n default
kubectl create clusterrolebinding squirrel-admin-binding -n default \
    --clusterrole cluster-admin \
    --serviceaccount default:squirrel

kubectl delete secret secrets-demo12 -n demo12
cat <<EOF | kubectl create -f -
apiVersion: v1
kind: Secret
metadata:
  name: secrets-demo12
  namespace: demo12
  annotations:
    squirrel: "true"
    squirrel_rotation_data: "pass, masterpass"
    squirrel_service: "pg-demo12"
    squirrel_username_key: "user"
    squirrel_password_key: "pass"
    squirrel_type_frontend: "odoo"
    squirrel_type_backend: "postgres"
    custom_database_name: "demo12"
    custom_database_port: "5432"
    custom_database_id: "2"
type: Opaque
data:
  user: b2Rvbw==
  pass: b2Rvbw==
  masterpass: b2Rvbw==
EOF


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

./main.py mode="client-create-key" key_file="local" email="juanmanuel.torres@aventurabinaria.es"

kubectl delete nutcrackers juanmanuel.torres
cat <<EOF | kubectl create -f -
apiVersion: "tree.squirrel.local/v1"
kind: Nutcrackers
metadata:
  name: juanmanuel.torres
type: Opaque
data:
  email: "juanmanuel.torres@aventurabinaria.es"
  keypub: $(cat $HOME/.squirrel/local.pub | base64 -w0)
permissions:
  - demo12/pg-demo12
  - demo11/pg-demo11
  - demo10/pg-demo10
EOF

python3 main.py mode="import-key" key-file="local.pub"
python3 main.py mode="list-keys"
python3 main.py mode="encrypt-text" email="juanmanuel.torres@aventurabinaria.es" text="hello"

cat <<EOF | kubectl create -f -
apiVersion: "tree.squirrel.local/v1"
kind: Nuts
metadata:
  name: juanmanuel.torres-test
type: Opaque
data:
  nut: $(echo "-----BEGIN PGP MESSAGE-----

hIwDhECx+42atRYBA/90cOl/WYBGi+38F/Op9kFnI2QQOyG1bUKJlC5ZJBJDeBf8
vOvWq2HsD7ZPvgMqHSOnRpmP7VZWMr1J5m5J9h06Rl8cNgPVaxxsJSJKQq7JsoqB
UJ9OonwtLjwuoquxpRLoPcpbJR6jAp4QGWeOS1/dfEqRM0bHkDbquTArGqupXtJV
AcpYfjJWaRtkgSmESmbLZcfPlFcJfT1eNOEg/RlyqTxBM2xncPIX5VCWuDr1W4Es
QAlsmvd2ju5H84PF0IQfv6+ZCX4xeubrZp8/k2fXJ9TSNk3g4g==
=Go6O
-----END PGP MESSAGE-----" | base64 -w0)
EOF

python3 main.py mode="cronjob"

