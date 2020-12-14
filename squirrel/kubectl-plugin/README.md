# Squirrel command

## Dependencies

```
sudo apt-get install sudo jq python3-gnupg xclip
pip3 install --user kubernetes pyperclip psycopg2
```

## Versions

Current
```
$ gpg --version
gpg (GnuPG) 1.4.20

$ pip3 freeze | grep gnupg
python-gnupg==0.3.8
```

Install ggp from: https://gnupg.org/ftp/gcrypt/gnupg/gnupg-1.4.20.tar.bz2
```
cd gnupg-1.4.20
./configure --prefix=/usr --libexecdir=/usr/lib
make
sudo make install
```

Install gnupg python version:
```
sudo apt purge python3-gnupg
pip3 install python-gnupg==0.3.8
```

Reset local key
```
squirrel drop-all
squirrel init 
```

## Install

```
curl -SL https://raw.githubusercontent.com/Tedezed/kubernetes-containers-tools/master/squirrel/kubectl-plugin/kubectl-squirrel -o kubectl-squirrel
chmod +x ./kubectl-squirrel
sudo cp ./kubectl-squirrel /usr/local/bin
```

For Bash
```
echo '
alias squirrel="/usr/local/bin/kubectl-squirrel"
source /usr/local/bin/kubectl-squirrel complete
' >> $HOME/.bashrc
```

For ZSH
```
echo '
squirrel() { PARAMETERS=$@; bash -c "/usr/local/bin/kubectl-squirrel $PARAMETERS" }
' >> $HOME/.zshrc
```

## Use

Need input email and password for create local keys (Before close terminal)
```
squirrel init
...
Email: [Enter email for gpg keys]
Password: [Enter password for gpg keys]

```
**Keys in $HOME/.squirrel/local.pub, send local.pub to admin.**

### Other commands

- `squirrel nuts`: See credentials for your email.
- `squirrel decrypt [NAME_NUT] [NAMESPACE_NUT]`: Decrypt message.
- `squirrel update`: Update comand squirrel.
- `squirrel drop-all`: Drop $HOME/.squirrel, including the keys.
