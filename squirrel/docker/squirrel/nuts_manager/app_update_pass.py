import psycopg2

class app_pass(squirrel_service, \
				squirrel_namespace, \
				squirrel_user, \
				squirrel_pass, \
				squirrel_type_frontend, \
				squirrel_type_backend):

	def __init__(self):
		app_pass_version="v0.1"

	def conditional_app(self):
		if squirrel_type_frontend == "odoo" \
		  and squirrel_type_backend == "postgres":
		  	odoo_postgres():

	def odoo_postgres(self):
		try:
		    connection = psycopg2.connect(user = "sysadmin",
		                                  password = "pynative@#29",
		                                  host = "127.0.0.1",
		                                  port = "5432",
		                                  database = "postgres_db")
		    cursor = connection.cursor()
		    # Print PostgreSQL Connection properties
		    print ( connection.get_dsn_parameters(),"\n")
		    # Print PostgreSQL version
		    cursor.execute("SELECT version();")
		    record = cursor.fetchone()
		    print("You are connected to - ", record,"\n")
		except (Exception, psycopg2.Error) as error :
		    print ("Error while connecting to PostgreSQL", error)
		finally:
		    #closing database connection.
		        if(connection):
		            cursor.close()
		            connection.close()
		            print("PostgreSQL connection is closed")
