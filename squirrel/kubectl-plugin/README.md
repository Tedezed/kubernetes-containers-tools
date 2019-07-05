# Squirrel command

## Dependencies

```
sudo apt-get install jq python3-gnupg xclip
pip3 install --user kubernetes pyperclip
```

## Install

```
curl -SL https://raw.githubusercontent.com/Tedezed/slug-containers/master/squirrel/kubectl-plugin/kubectl-squirrel -o kubectl-squirrel
chmod +x ./kubectl-squirrel
sudo cp ./kubectl-squirrel /usr/local/bin
echo '
alias squirrel="/usr/local/bin/kubectl-squirrel"
source /usr/local/bin/kubectl-squirrel
' >> $HOME/.bashrc
```

## Use

Need input email and password for create local keys 
```
squirrel init
...
Email: [Enter email for gpg keys]
Password: [Enter password for gpg keys]
```


