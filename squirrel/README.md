# Squirrel

Rotation of passwords and storage using gpg for applications in Kubernetes

<img src="https://raw.githubusercontent.com/tedezed/slug-containers/master/docs/img/Squirrel.png">

# Install

```
kubectl create -f https://raw.githubusercontent.com/Tedezed/slug-containers/master/squirrel/install.yaml
```

## Create Nutcrackers

Example Admin:
```
kubectl delete nutcrackers admin
cat <<EOF | kubectl create -f -
apiVersion: "tree.squirrel.local/v1"
kind: Nutcrackers
metadata:
  name: admin
type: Opaque
data:
  email: "admin@example.com"
  keypub: $(cat $HOME/.squirrel/local.pub | base64 -w0)
permissions:
  - "*/*"
EOF
```

Example User:
```
kubectl delete nutcrackers user
cat <<EOF | kubectl create -f -
apiVersion: "tree.squirrel.local/v1"
kind: Nutcrackers
metadata:
  name: admin
type: Opaque
data:
  email: "user@example.com"
  keypub: $(cat $HOME/.squirrel/local.pub | base64 -w0)
permissions:
  # - "namespace/service"
  - "demo1/app-demo1"
  - "demo2/app-demo2"
EOF
```