import psycopg2, base64
from passlib.hash import pbkdf2_sha512

class app_update_pass():

    def __init__(self,
                squirrel_service,
                squirrel_namespace,
                squirrel_user,
                squirrel_pass,
                squirrel_type_frontend,
                squirrel_type_backend,
                secret_annotations,
                mode,
                random_pass):

        app_pass_version="v0.1"
        self.squirrel_mode = mode
        self.squirrel_service = squirrel_service
        self.squirrel_namespace = squirrel_namespace
        self.squirrel_user = base64.b64decode(\
            squirrel_user + '=' * (-len(squirrel_user) % 4)).decode()
        self.squirrel_pass = base64.b64decode(\
            squirrel_pass + '=' * (-len(squirrel_pass) % 4)).decode()
        self.squirrel_type_frontend = squirrel_type_frontend
        self.squirrel_type_backend = squirrel_type_backend
        self.secret_annotations = secret_annotations
        self.random_pass = random_pass
        self.host = "%s.%s.svc.cluster.local" % \
          (squirrel_service, squirrel_namespace)

    def conditional_app(self):
        if self.squirrel_type_frontend == "odoo" \
          and self.squirrel_type_backend == "postgres" \
          and self.squirrel_mode == "update_app_password":
              self.odoo_postgresv2()
        elif self.squirrel_type_frontend == "odoo" \
          and self.squirrel_type_backend == "postgres" \
          and self.squirrel_mode == "update_secret":
              self.postgres_password_update()

    def postgres_execution(self, 
                           name_username,
                           user_password,
                           postgres_host,
                           postgres_port,
                           name_database,
                           list_querys):
        try:
            connection = psycopg2.connect(user = name_username,
                                          password = user_password,
                                          host = postgres_host,
                                          database = name_database,
                                          port = postgres_port)
            cursor = connection.cursor()
            #record = cursor.fetchone()
            for query in list_querys:
                cursor.execute(query)
            connection.commit()
            print("[INFO] %s successfully" % cursor.rowcount)
        except (Exception, psycopg2.Error) as error:
            print ("Error while connecting to PostgreSQL: ", error)
            return False
        finally:
            if 'connection' in locals():
                if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")
            return True

    def odoo_postgresv2(self):
        try:
            print("[INFO] Postgres update password")
            database = self.secret_annotations.get("custom_database_name", "odoo")
            port = self.secret_annotations.get("custom_database_port", "5432")
            id_update_pass = self.secret_annotations.get("custom_database_id", False)
            if id_update_pass:
                pass_hash = pbkdf2_sha512.hash(self.random_pass)
                update_query = ["UPDATE res_users set password='%s' WHERE id=%s;" \
                    % (pass_hash, id_update_pass)]
                self.postgres_execution(self.squirrel_user, self.squirrel_pass, \
                    self.host, port, database, update_query)
        except Exception as e:
            print("[ERROR] %s" % error)


    def postgres_password_update(self):
        try:
            print("[INFO] Postgres update password for user %s" % self.squirrel_user)
            database = "postgres"
            port = self.secret_annotations.get("custom_database_port", "5432")
            alter_query = ["ALTER USER %s WITH PASSWORD '%s';" \
                % (self.squirrel_user, self.random_pass)]
            #print(alter_query)
            #print(self.squirrel_user, self.squirrel_pass)
            self.postgres_execution(self.squirrel_user, self.squirrel_pass, \
                self.host, port, database, alter_query)
        except Exception as e:
            print("[ERROR] %s" % error)

