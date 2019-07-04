# Kubectl Plugin

## Dependencies

```
sudo apt-get install jq python3-gnupg
pip3 install --user kubernetes
```

## Install

```
curl -SL https://raw.githubusercontent.com/Tedezed/slug-containers/master/squirrel/kubectl-plugin/kubectl-squirrel -o kubectl-squirrel
chmod +x ./kubectl-squirrel
sudo cp ./kubectl-squirrel /usr/local/bin
```

## Use

Need input email and password for create local keys 
```
kubectl squirrel init
...
Email: [Enter email for gpg keys]
Password: [Enter password for gpg keys]
```


