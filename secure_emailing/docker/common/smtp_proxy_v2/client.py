import smtplib

msg = """From: foo@demo1.com
To: bar@localhost

Here's my message!
"""
user = 'demo'
passwd = 'demo'

server = smtplib.SMTP('localhost', port=1025)
server.set_debuglevel(1)
server.login(user, passwd)
server.sendmail('foo@fff.com', ['bar@localhost'], msg)
server.quit()
