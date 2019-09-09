import psycopg2, base64, sys, os, ast, importlib, socket
from passlib.hash import pbkdf2_sha512

class squirrel_module():

    def __init__(self, squirrel):
        self.squirrel = squirrel
        name = "Odoo/Postgres Squirrel Module"
        self.squirrel_service = squirrel.squirrel_service
        self.squirrel_namespace = squirrel.squirrel_namespace
        self.squirrel_user = squirrel.squirrel_user
        self.squirrel_pass = squirrel.squirrel_pass
        self.secret_annotations = squirrel.secret_annotations
        self.random_pass = squirrel.random_pass
        self.host = squirrel.host
        self.debug_mode = squirrel.debug_mode

    def postgres_execution(self,
                           name_username,
                           user_password,
                           postgres_host,
                           postgres_port,
                           name_database,
                           list_querys):

        print("[INFO] Postgres - Host: %s" % (postgres_host))
        #ip_host = socket.gethostbyname(postgres_host)
        #print("[INFO Postgres - IP: %s]" % (ip_host))
        dic_query = {}
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
                try:
                    dic_query[query] = cursor.fetchall()
                except Exception as e:
                    print("(postgres_execution)[WARNING] fetchall: %s" % e)
            connection.commit()
            print("(postgres_execution)[INFO] %s successfully" % cursor.rowcount)
        except (Exception, psycopg2.Error) as error:
            print("(postgres_execution)[ERROR] while connecting to PostgreSQL: ", error)
        finally:
            if 'connection' in locals():
                if(connection):
                    cursor.close()
                    connection.close()
                    print("(postgres_execution)[INFO] PostgreSQL connection is closed")
            return dic_query

    def update_app(self):
        system_databases = ["postgres", "template1", "template0"]
        try:
            print("(odoo_postgresv2)[INFO](init) Postgres update user Odoo password")
            database = self.secret_annotations.get("custom_database_name", "odoo")
            port = self.secret_annotations.get("custom_database_port", "5432")
            query = ["SELECT datname FROM pg_catalog.pg_database;"]
            list_databases = self.postgres_execution(self.squirrel_user, self.squirrel_pass, \
                self.host, port, "postgres", query)
            databases = database.replace(" ", "")
            databases = databases.split(",")
            for d_name in databases:
                for d in list_databases[query[0]]:
                    if d[0] not in system_databases:
                        if d[0] == d_name or d_name == "*":
                            print("(odoo_postgresv2)[INFO] Processing database %s" % d[0])
                            query_version_odoo = ["SELECT latest_version FROM ir_module_module WHERE name = 'base';"]
                            version_odoo = self.postgres_execution(self.squirrel_user, self.squirrel_pass, \
                                self.host, port, d[0], query_version_odoo)
                            valid_odoo_version = True
                            if version_odoo and version_odoo[query_version_odoo[0]]:
                                output_version = int(version_odoo[query_version_odoo[0]][0][0].split(".")[0])
                                pass_hash = pbkdf2_sha512.hash(self.random_pass)
                                if output_version >= 12:
                                    update_query = ["UPDATE res_users set password='%s' WHERE id=2;" \
                                        % (pass_hash)]
                                elif output_version < 12 and output_version > 7:
                                    update_query = ["UPDATE res_users set password_crypt='%s' WHERE id=1;" \
                                        % (pass_hash)]
                                elif output_version <= 7:
                                    update_query = ["UPDATE res_users set password='%s' WHERE id=1;" \
                                        % (self.random_pass)]
                                else:
                                    valid_odoo_version = False
                                if valid_odoo_version:
                                    if not self.debug_mode:
                                        self.postgres_execution(self.squirrel_user, self.squirrel_pass, \
                                            self.host, port, d[0], update_query)
                                    print("(odoo_postgresv2)[INFO] Successful update in database %s" % d[0])
                                else:
                                    print("(odoo_postgresv2)[ERROR] Not valid Odoo version found")
                            else:
                                print("(odoo_postgresv2)[ERROR] Not valid database Odoo")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("(odoo_postgresv2)[ERROR] %s, file: %s. line: %s" % (e, fname, exc_tb.tb_lineno))
            return False
        return True


    def update_secret(self):
        try:
            print("(postgres_password_update)[INFO] Postgres update password for user %s" % self.squirrel_user)
            database = "postgres"
            port = self.secret_annotations.get("custom_database_port", "5432")
            alter_query = ["ALTER USER %s WITH PASSWORD '%s';" \
                % (self.squirrel_user, self.random_pass)]
            #print(alter_query)
            #print(self.squirrel_user, self.squirrel_pass)
            if not self.debug_mode:
                self.postgres_execution(self.squirrel_user, self.squirrel_pass, \
                    self.host, port, database, alter_query)
        except Exception as e:
            print("(postgres_password_update)[ERROR] %s" % error)
            return False
        return True

