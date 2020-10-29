cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  labels:
    app: nginx-error
    provider: nginx-error
  name: nginx-error
  namespace: nginx-ingress
spec:
  ports:
  - port: 80
  selector:
    app: nginx-error
  type: ClusterIP
---
apiVersion: v1
kind: ReplicationController
metadata:
  labels:
    app: nginx-error
    heritage: helm
  name: nginx-error
  namespace: nginx-ingress
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: nginx-error
    spec:
      containers:
      - name: nginx-error
        image: tedezed/nginx-error:latest
        ports:
        - containerPort: 80
EOF