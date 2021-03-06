# Custom APT repository

### Sources

- https://wiki.debian.org/DebianRepository/SetupWithReprepro
- https://www.howtoforge.com/setting-up-an-apt-repository-with-reprepro-and-nginx-on-debian-wheezy

### Install
```
kubectl create -f https://github.com/Tedezed/kubernetes-containers-tools/blob/master/apt-repository/kube/main.yaml
```

### Clone and add new packages

Clone one by one
```
curl -SL http://ftp.us.debian.org/debian/pool/main/p/python3.7/python3.7_3.7.3-2+deb10u1_amd64.deb -o /usr/src/pagespeed/python3.7_3.7.3-2+deb10u1_amd64.deb
```

Clone using for:
```
URL="http://ftp.us.debian.org/debian/pool/main/p/python3.7/"
for deb in $(curl $URL | grep -o 'href=".*.deb"' | grep "amd64" | cut -d '"' -f2 ); do
	curl -SL $URL$deb -o /usr/src/pagespeed/$deb
done
```

Clone all python for example:
```
URL="http://ftp.us.debian.org/debian/pool/main/p/"
DEB_INCLUDE="amd64\|all"
#GET="href=\"python.*\""
GET="href=\"python[2-3]\..*\""
for package in $(curl http://ftp.us.debian.org/debian/pool/main/p/ | grep -o "$GET" | cut -d '"' -f2 ); do
	echo "[INFO] Package: $(echo $package | cut -d '/' -f1)"
	for deb in $(curl $URL$package | grep -o 'href=".*.deb"' | grep "$DEB_INCLUDE" | cut -d '"' -f2 ); do
		echo "[INFO] Deb: $deb"
		curl -SL $URL$package$deb -o /usr/src/pagespeed/$deb
	done
done
```

Add new packages:
```
export GPG_TTY=$(tty)
dpkg-sig -k $(gpg --list-secret-keys --with-colons --fingerprint | grep ssb | cut -d ":" -f 5) --sign builder /usr/src/pagespeed/*.deb
cd /var/packages/debian
reprepro includedeb testing /usr/src/pagespeed/*.deb
```

### Add your own repository

`nano /etc/apt/sources.list`
```
deb http://apt.example.com/debian/ testing main
```

If you want this repository to always have precedence over other repositories
`nano /etc/apt/preferences`
```
Package: *
Pin: origin apt.example.com
Pin-Priority: 1001
```

Add key: `wget -O - -q http://apt.example.com/apt.example.com.gpg.key | apt-key add - `

Update and use
```
apt-get update
apt-get install your_package -y
```