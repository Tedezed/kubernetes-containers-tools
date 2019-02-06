# Secure Emailing

Based on: https://github.com/bcoe/secure-smtpd

```
   -----------                                      --------------------
  |  Mailjet  | --------------------Port: 25-----> | Destination Server |
   -----------                                      --------------------
       ^
       | Port: 2525
       |
       |
 ----------------- 
|[Cloud  Firewall]| (Close egress port 25)
 ----------------- 
       ^
       | Port: 2525
       |
       |
 ---------------
|  Relay email  | // tcpdump -i eth0 'port 25'
 ---------------
       ^
       | Port: 25
       |
 ----------------                             --------------
|  Secure email  | <---- Port: 5432 -------> |  PostgreSQL  |
 ----------------                             --------------
       ^
       | Port: 9000
       |
 ---------------
|  Client SMTP  |  
 ---------------

```