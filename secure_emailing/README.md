# Secure Emailing

### Control of permissions for SMTP relay.

- Problem with GCP (Port 25 is always blocked and cannot be used): https://cloud.google.com/compute/docs/tutorials/sending-mail/
- Based on: https://github.com/bcoe/secure-smtpd

#### Process of sending mail and internal verification of permissions

<img src="https://raw.githubusercontent.com/Tedezed/kubernetes-containers-tools/master/docs/img/secure_email_working.png">

## Example usage

Create user test1:
```
# mailadmin add user test1
password: 
```

Create address user@test1.com:
```
# mailadmin add address user@test1.com
```

Create domain test1.com:
```
# mailadmin add domain test1.com
```

Grant send emails with address user@test1.com to user test1:
```
# mailadmin grant address user@test1.com to test1
```

Grant send emails with domain @test1.com to user test1:
```
# mailadmin grant domain test1.com to test1
```

List users:
```
# mailadmin list users 
--- emailing_users ---
    - demo
    - test1
    - test2
```

List addresses:
```
# mailadmin list addresses 
--- emailing_addresses ---
    - user@demo.com
    - user@test1.com
```

List domains:
```
# mailadmin list domains 
--- emailing_domains ---
    - test1.com
```

Show users with permissions on address user@test1.com:
```
# mailadmin show address user@test1.com
--- Show user@test1.com ---
  Users:
    * test1
    * test2
```

Show users with permissions on domain @test1.com:
```
# mailadmin show domain test1.com
--- Show test1.com ---
  Users:
    * test1
    * test2
```

Show permissions of the user test1:
User test1 can send emails with address user@test1.com and all address of domain @test1.com.
```
# mailadmin show user test1
--- Show test1 ---
  Domains:
    * test1.com
  Adress:
    * user@test1.com
```


## Test permissions

```
kubectl port-forward $(kubectl get pod --all-namespaces | grep "secure-emailing" | grep -v "pg" | awk '{ print $2 }') -n kube-system 9000:9000
```

Can send email with address user@test1.com and user test1:
```
python smtp_proxy_v2/test.py senmail localhost 9000 test1 passtest1 user@test1.com 'TEST-MAIL' 'DESTINATION_EMAIL@gmail.com' 'Hi! test-mail'
```

Can not send email with address user@demo.com and user test1:
```
python smtp_proxy_v2/test.py senmail localhost 9000 test1 passtest1 user@demo.com 'TEST-MAIL' 'DESTINATION_EMAIL@gmail.com' 'Hi! test-mail'
```

## Database design

<img src="https://raw.githubusercontent.com/Tedezed/kubernetes-containers-tools/master/docs/img/secure_emailing.png">
