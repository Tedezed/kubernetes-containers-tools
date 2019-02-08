import sys

from credentials_emailing import StoreCredentials

import smtplib, sys, os
from email.mime.text import MIMEText

def example_execution(num=1):
	if num == 1:
		print("""Example: python smtp_proxy_v2/test.py [TEST]

  - validatemail
  - senmail
	""")
	elif num == 2:
		print("""Example: python smtp_proxy_v2/test.py senmail MAIL_SERVER \
			MAIL_SERVER_PORT USER PASS YOUR_EMAIL DESTINATION_EMAIL \
			SUBJECT MESSAGE""")
	elif num == 3:
		print("""Example: python smtp_proxy_v2/test.py validatemail \
			DESTINATION_EMAIL USER PASS""")

if len(sys.argv) > 1:
	if sys.argv[1] == "validatemail":
		print("Test: Validatemail using StoreCredentials")
		st = StoreCredentials()
		target = sys.argv[2]
		user = sys.argv[3]
		passwd = sys.argv[4]
		print(st.validate_mailfrom(target, user, passwd))

	elif sys.argv[1] == "senmail":
		print("Test: Send mail to server")

		mailserver = sys.argv[2]
		mailport = int(sys.argv[3])

		user = sys.argv[4]
		passwd = sys.argv[5]

		from_email = sys.argv[6]
		sub = sys.argv[7]
		targets = [sys.argv[8]]
		txt = sys.argv[9]

		#targets = os.environ['MAIL_TARGETS'].replace('"', ' ').split(",")
		targetscorrect = []
		for mail in targets:
			date = mail.split()
			targetscorrect.append(date[0])

		server = smtplib.SMTP(str(mailserver), str(mailport))
		server.ehlo()
		try:
			server.starttls()
			server.ehlo()
		except:
			server.ehlo()
			print('[WARNING] Server not support tls')

		try:
			server.login(user, passwd)
		except:
			print('[WARNING] Server not support login')

		msg = MIMEText(txt, "html")
		msg['Subject'] = sub
		msg['From'] = from_email
		msg['To'] = ', '.join(targetscorrect)

		print "txt: %s" % txt
		if txt != "":
			for t in targets:
				print "Send mail to "+t
				server.sendmail(from_email, t, msg.as_string())
	else:
		example_execution()
else:
	example_execution()