import smtplib

# Server
server_smtp = 'localhost'
server_port = 1025

# User secure SMTP
user = 'demo'
passwd = 'demo'

# Msg info
sender = 'foo@demo1.com'
receivers = 'bar@localhost'
txt = "Here's my message!"

msg = """From: %s
To: %s

%s
""" % (sender, receivers, txt)

server = smtplib.SMTP(server_smtp, port=server_port)
server.set_debuglevel(1)
server.login(user, passwd)
server.sendmail(sender, receivers, msg)
server.quit()
