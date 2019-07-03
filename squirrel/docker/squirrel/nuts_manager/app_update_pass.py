import psycopg2, base64
from passlib.hash import pbkdf2_sha512

class app_update_pass():

    def __init__(self, \
                    squirrel_service, \
                    squirrel_namespace, \
                    squirrel_user, \
                    squirrel_pass, \
                    squirrel_type_frontend, \
                    squirrel_type_backend,
                    secret_annotations,
                    random_pass):

        app_pass_version="v0.1"
        self.squirrel_service = squirrel_service
        self.squirrel_namespace = squirrel_namespace
        self.squirrel_user = squirrel_user
        self.squirrel_pass = squirrel_pass
        self.squirrel_type_frontend = squirrel_type_frontend
        self.squirrel_type_backend = squirrel_type_backend
        self.secret_annotations = secret_annotations
        self.random_pass = random_pass

    def conditional_app(self):
        if self.squirrel_type_frontend == "odoo" \
          and self.squirrel_type_backend == "postgres":
              self.odoo_postgres()

    # Example Odoo512
    def odoo_postgres(self):
    	# https://passlib.readthedocs.io/en/stable/
    	# https://docs.python.org/2/library/hashlib.html
        try:
            connection = psycopg2.connect(user = base64.b64decode(self.squirrel_user + '=' * (-len(self.squirrel_user) % 4)).decode(),
                                          password = base64.b64decode(self.squirrel_pass + '=' * (-len(self.squirrel_pass) % 4)).decode(),
                                          host = "%s.%s.svc.cluster.local" % (self.squirrel_service, self.squirrel_namespace),
                                          database = self.secret_annotations.get("custom_database_name", "odoo"),
                                          port = self.secret_annotations.get("custom_database_port", "5432"))
            cursor = connection.cursor()
            # Print PostgreSQL Connection properties
            print(connection.get_dsn_parameters(),"\n")
            # Print PostgreSQL version
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("You are connected to - ", record,"\n")

            id_update_pass = self.secret_annotations.get("custom_database_id", False)
            if id_update_pass:
                pass_hash = pbkdf2_sha512.hash(self.random_pass)
                update_query = "UPDATE res_users set password='%s' WHERE id=%s;" % (pass_hash, id_update_pass)
                print(update_query)
                cursor.execute(update_query)
                connection.commit()
                count = cursor.rowcount
                print(count, "Record Updated successfully ")
            else:
                raise Exception("[ERROR] Annotations custom_database_id not found in secret")
                return True
           
        except (Exception, psycopg2.Error) as error:
            print ("Error while connecting to PostgreSQL: ", error)
            return True
        finally:
            #closing database connection.
                if 'connection' in locals():
                    if(connection):
                        cursor.close()
                        connection.close()
                        print("PostgreSQL connection is closed")
                        return False
