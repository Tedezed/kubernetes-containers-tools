import psycopg2, psycopg2.extras, hashlib, sys, getpass
from ConfigParser import SafeConfigParser
from os import path, getlogin, system, getuid, environ

ruta_exec = path.dirname(path.realpath(__file__))
parser = SafeConfigParser()
parser.read(ruta_exec + '/emailing.conf')
db_name = parser.get('POSTGRES', 'db_name')
db_user = parser.get('POSTGRES', 'db_user')
db_passwd = parser.get('POSTGRES', 'db_passwd')
db_host = parser.get('POSTGRES', 'db_host')

conn = psycopg2.connect(database=db_name ,user=db_user, password=db_passwd, host=db_host)

def validate(name, type_select):
	if type_select == "domain":
		table = "emailing_domains"
		column = "domain"
	elif type_select == "user":
		table = "emailing_users"
		column = "name"
	elif type_select == "address":
		table = "emailing_addresses"
		column = "address"
	cur = conn.cursor()
	cur.execute("SELECT id FROM %s WHERE %s='%s'" % (table, column, name))
	id_internal = cur.fetchone()
	cur.close()
	if id_internal == [] or id_internal == None:
		return False
	else:
		return True

def list_all(command, type_select):
	if type_select == "domain":
		table = "emailing_domains"
		column = "domain"
	elif type_select == "user":
		table = "emailing_users"
		column = "name"
	elif type_select == "address":
		table = "emailing_addresses"
		column = "address"
	cur = conn.cursor()
	cur.execute("SELECT %s FROM %s" % (column, table))
	users = cur.fetchall()
	print "--- %s ---" % table
	for u in users:
		print "    - %s" % u[0]
	cur.close()

def show_user(command):
	name_user = command.split(" ")[2]
	if validate(name_user, "user"):
		print "--- Show %s ---" % name_user
		cur = conn.cursor()
		cur.execute("""SELECT domain
		            FROM emailing_domains
		            WHERE id IN (SELECT id_domain
		                         FROM emailing_users_domains
		                         WHERE id_user = (SELECT id FROM emailing_users WHERE name = '%s'))""" % name_user)
		domains = cur.fetchall()

		cur.execute("""SELECT address
		                FROM emailing_addresses
		                WHERE id IN (SELECT id_address
		                         FROM emailing_users_addresses
		                         WHERE id_user = (SELECT id FROM emailing_users WHERE name = '%s'))""" % name_user)
		address = cur.fetchall()
		cur.close()
		print "  Domains:"
		for d in domains:
			print "    * %s" % d[0]
		print "  Adress:"
		for a in address:
			print "    * %s" % a[0]
	else:
		print "%s not found" % name_user

def show(command, type_select):
	if type_select == "domain":
		table = "emailing_domains"
		column = "domain"
		table_check = "emailing_users_domains"
		column_check = "id_domain"
	elif type_select == "address":
		table = "emailing_addresses"
		column = "address"
		table_check = "emailing_users_addresses"
		column_check = "id_address"
	name = command.split(" ")[2]
	if validate(name, type_select):
		print "--- Show %s ---" % name
		cur = conn.cursor()
		cur.execute("""SELECT name
		            FROM emailing_users
		            WHERE id IN (SELECT id_user
		                         FROM %s
		                         WHERE %s = (SELECT id FROM %s WHERE %s = '%s'))""" % (table_check, column_check, table, column, name))
		users = cur.fetchall()
		cur.close()

		print "  Users:"
		for u in users:
			print "    * %s" % u[0]
	else:
		print "%s not found" % name

def add_user(command):
	name_user = command.split(" ")[2]
	if validate(name_user, "user"):
		print "User %s exist" % name_user
	else:
		password = getpass.getpass("password: ")
		hash_object = hashlib.md5(password)
		pass_user_external = hash_object.hexdigest()

		cur = conn.cursor()
		cur.execute("SELECT max(id) FROM emailing_users")
		next_id = cur.fetchone()[0] + 1
		cur.execute("INSERT INTO emailing_users (id, name, passwd) VALUES (%s, '%s', '%s')" % (next_id, name_user, pass_user_external))
		cur.close()

def add_domain(command):
	name_domain = command.split(" ")[2]
	if validate(name_domain, "domain"):
		print "Domain %s exist" % name_domain
	else:
		cur = conn.cursor()
		cur.execute("SELECT max(id) FROM emailing_domains")
		next_id = cur.fetchone()[0] + 1
		cur.execute("INSERT INTO emailing_domains (id, domain) VALUES (%s, '%s')" % (next_id, name_domain))
		cur.close()

def add_address(command):
	name_address = command.split(" ")[2]
	if validate(name_address, "address"):
		print "Adress %s exist" % name_address
	else:
		cur = conn.cursor()
		cur.execute("SELECT max(id) FROM emailing_addresses")
		next_id = cur.fetchone()[0] + 1
		cur.execute("INSERT INTO emailing_addresses (id, address) VALUES (%s, '%s')" % (next_id, name_address))
		cur.close()

def add_domain_to_user(command):
	name_domain = command.split(" ")[2]
	name_user = command.split(" ")[4]
	if validate(name_domain, "domain") and validate(name_user, "user"):
		# grant domain scalpers.com to jonh
		cur = conn.cursor()
		cur.execute("SELECT id FROM emailing_users WHERE name = '%s'" % name_user)
		id_user = cur.fetchone()[0]
		cur.execute("SELECT id FROM emailing_domains WHERE domain = '%s'" % name_domain)
		id_domain = cur.fetchone()[0]
		cur.execute("SELECT id_user FROM emailing_users_domains WHERE id_user=%s AND id_domain=%s" % (id_user, id_domain))
		validate_ids = cur.fetchone()
		if validate_ids == [] or validate_ids == None:
			cur.execute("INSERT INTO emailing_users_domains (id_user, id_domain) VALUES (%s, %s)" % (id_user, id_domain))
			cur.close()
		else:
			print "User %s has permission to %s" % (name_user, name_domain)
	else:
		print "Domain or user not exist"

def add_address_to_user(command):
	name_address = command.split(" ")[2]
	name_user = command.split(" ")[4]
	if validate(name_address, "address") and validate(name_user, "user"):
		# grant domain scalpers.com to jonh
		cur = conn.cursor()
		cur.execute("SELECT id FROM emailing_users WHERE name = '%s'" % name_user)
		id_user = cur.fetchone()[0]
		cur.execute("SELECT id FROM emailing_addresses WHERE address = '%s'" % name_address)
		id_address = cur.fetchone()[0]
		cur.execute("SELECT id_user FROM emailing_users_addresses WHERE id_user=%s AND id_address=%s" % (id_user, id_address))
		validate_ids = cur.fetchone()
		if validate_ids == [] or validate_ids == None:
			cur.execute("INSERT INTO emailing_users_addresses (id_user, id_address) VALUES (%s, %s)" % (id_user, id_address))
			cur.close()
		else:
			print "User %s has permission to %s" % (name_user, name_address)
	else:
		print "Address or user not exist"

def del_user(command):
	name_user = command.split(" ")[2]
	if validate(name_user, "user"):
		cur = conn.cursor()
		cur.execute("""DELETE FROM emailing_users_addresses
						WHERE id_user = (SELECT id 
									FROM emailing_users
									WHERE name = '%s')""" \
									% (name_user))
		cur.execute("""DELETE FROM emailing_users_domains
						WHERE id_user = (SELECT id 
									FROM emailing_users
									WHERE name = '%s')""" \
									% (name_user))
		cur.execute("""DELETE FROM emailing_users
				WHERE id = (SELECT id 
							FROM emailing_users
							WHERE name = '%s')""" \
							% (name_user))
		cur.close()
	else:
		print "User %s not exist" % name_user

def del_domain(command):
	name_domain = command.split(" ")[2]
	if validate(name_domain, "domain"):
		cur = conn.cursor()
		cur.execute("""DELETE FROM emailing_users_domains
				WHERE id_domain = (SELECT id 
							FROM emailing_domains
							WHERE domain = '%s');""" \
							% (name_domain))
		cur.execute("""DELETE FROM emailing_domains
						WHERE id = (SELECT id 
									FROM emailing_domains
									WHERE domain = '%s')""" \
									% (name_domain))
		cur.close()
	else:
		print "Domain %s not exist" % name_domain

def del_address(command):
	name_address = command.split(" ")[2]
	if validate(name_address, "address"):
		cur = conn.cursor()
		cur.execute("""DELETE FROM emailing_users_addresses
						WHERE id_address = (SELECT id 
									FROM emailing_addresses
									WHERE address = '%s')""" \
									% (name_address))
		cur.execute("""DELETE FROM emailing_addresses
						WHERE id = (SELECT id 
									FROM emailing_addresses
									WHERE address = '%s')""" \
									% (name_address))
		cur.close()
	else:
		print "Adress %s not exist" % name_address

def help():
	print """Mailadmin
  Commnads:
    * list users - List all users
    * list domains - List all domains
    * list addresses - List all addresses
    * show user USER - Show permission to user
    * show domain DOMAIN - Show users with permission to domain
    * show address ADDRESS - Show users with permission to address
    * add user USER - Add user to database
    * add domain DOMAIN - Add addres to database
    * add address ADDRESS - Add addres to database
    * grant domain DOMAIN to USER - Grant domain to user
    * grant address ADDRESS to USER - Grant addres to user"""

list_init = sys.argv
key = True
while key:
	# Command mode
	if len(list_init) > 1:
		command_list = list_init[:]
		del command_list[0]
		command = ' '.join(command_list)
	else:
		command = raw_input("> ")

	# Normal mode
	command = command.lower()
	if "exit" == command:
		print "Bye"
		key = False
	elif key == "":
		pass
	elif "help" == command:
		help()

	if len(command.split(" ")) > 1:
		try:
			if "list domains" == "%s %s" % (command.split(" ")[0], command.split(" ")[1]):
				list_all(command, "domain")
			elif "list users" == "%s %s" % (command.split(" ")[0], command.split(" ")[1]):
				list_all(command, "user")
			elif "list addresses" == "%s %s" % (command.split(" ")[0], command.split(" ")[1]):
				list_all(command, "address")
			elif "show user" == "%s %s" % (command.split(" ")[0], command.split(" ")[1]):
				show_user(command)
			elif "show domain" == "%s %s" % (command.split(" ")[0], command.split(" ")[1]):
				show(command, "domain")
			elif "show address" == "%s %s" % (command.split(" ")[0], command.split(" ")[1]):
				show(command, "address")
			elif "add user" == "%s %s" % (command.split(" ")[0], command.split(" ")[1]):
				add_user(command)
			elif "add domain" == "%s %s" % (command.split(" ")[0], command.split(" ")[1]):
				add_domain(command)
			elif "add address" == "%s %s" % (command.split(" ")[0], command.split(" ")[1]):
				add_address(command)
			elif "grant domain" == "%s %s" % (command.split(" ")[0], command.split(" ")[1]):
				add_domain_to_user(command)
			elif "grant address" == "%s %s" % (command.split(" ")[0], command.split(" ")[1]):
				add_address_to_user(command)
			elif "del user" == "%s %s" % (command.split(" ")[0], command.split(" ")[1]):
				del_user(command)
			elif "del domain" == "%s %s" % (command.split(" ")[0], command.split(" ")[1]):
				del_domain(command)
			elif "del address" == "%s %s" % (command.split(" ")[0], command.split(" ")[1]):
				del_address(command)
			else:
				print "Unrecognized command %s" % command
			# Commit	
			conn.commit()
		except Exception as e:
			print "[ERROR] %s" % e

	# Command mode
	if len(list_init) > 1:
		key = False

conn.close()