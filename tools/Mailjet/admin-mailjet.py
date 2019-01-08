# https://github.com/mailjet/mailjet-apiv3-python
# https://dev.mailjet.com/reference/email/sender-addresses-and-domains/sender/

import os, json
try:
	from mailjet_rest import Client
except ImportError as e:
	print "ERROR: %s" % (e)
	print "Install library from: https://github.com/mailjet/mailjet-apiv3-python"
	exit()

def clean_inactive_senders(mailjet, MJ_APIKEY_PUBLIC, MJ_APIKEY_PRIVATE):
	result = mailjet.sender.get(filters={'Limit': '1000'})
	dic_contacts = json.loads(result.text)
	list_delete_ids = []
	for t in dic_contacts["Data"]:
		id_contact = t["ID"]
		sender_email = t["Email"]
		status = t["Status"]
		# t["Filename"] identify domains
		if status == "Inactive" and t["Filename"] == "":
			print "ID: %s - Delete sender: %s " % (id_contact, sender_email)
			list_delete_ids.append(id_contact)

	if list_delete_ids != []:
		confirm_delete = ""
		while confirm_delete != "y" and confirm_delete != "n":
			confirm_delete = raw_input("Confirm for delete (y/n): ")
		if confirm_delete == "y":
			for id_sender in list_delete_ids:
				print "Delete sender with ID %s..." % (id_sender)
				result = mailjet.sender.delete(id_sender)
				print result.text
		else:
			print "Not delete senders"
	else:
		print "No inactive senders were found"

# Get your environment Mailjet keys
MJ_APIKEY_PUBLIC = os.environ['MJ_APIKEY_PUBLIC']
MJ_APIKEY_PRIVATE = os.environ['MJ_APIKEY_PRIVATE']

mailjet = Client(auth=(MJ_APIKEY_PUBLIC, MJ_APIKEY_PRIVATE), version='v3')

help_text = """Commands:
	- help
	- clean-senders (clean inactive senders)
	- exit
"""

command = ""
while command != "exit":
	command = raw_input("admin-mailjet> ")
	if command == "help":
		print help_text
	elif command == "clean-senders":
		clean_inactive_senders(mailjet, MJ_APIKEY_PUBLIC, MJ_APIKEY_PRIVATE)
	elif command == "exit":
		pass
	else:
		print "Command not found"
print "bye"
