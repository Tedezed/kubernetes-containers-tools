import pymysql

class squirrel_module():

    def __init__(self, squirrel):
        self.squirrel = squirrel
        self.squirrel_service = squirrel.squirrel_service
        self.squirrel_namespace = squirrel.squirrel_namespace
        self.squirrel_user = squirrel.squirrel_user
        self.squirrel_pass = squirrel.squirrel_pass
        self.secret_annotations = squirrel.secret_annotations
        self.random_pass = squirrel.random_pass
        self.host = squirrel.host
        self.debug_mode = squirrel.debug_mode

    def mysql_execution(self,
                           name_username,
                           user_password,
                           mysql_host,
                           mysql_port,
                           name_database,
                           list_querys):

        print("[INFO] Mysql - Host: %s" % (mysql_host))
        dic_query = {}
        try:
            connection = pymysql.connect(user = name_username,
                                          password = user_password,
                                          host = mysql_host,
                                          database = name_database,
                                          port = mysql_port)
            cursor = connection.cursor()
            #record = cursor.fetchone()
            for query in list_querys:
                cursor.execute(query)
                try:
                    dic_query[query] = cursor.fetchall()
                except Exception as e:
                    print("(mysql_execution)[WARNING] fetchall: %s" % e)
            connection.commit()
            print("(mysql_execution)[INFO] %s successfully" % cursor.rowcount)
        except (Exception, pymysql.Error) as error:
            print("(mysql_execution)[ERROR] while connecting to MySQL: ", error)
        finally:
            if 'connection' in locals():
                if(connection):
                    cursor.close()
                    connection.close()
                    print("(mysql_execution)[INFO] MySQL connection is closed")
            return dic_query

    def update_app(self):
        print("update app")
        # if is OK
        return True

    def update_secret(self):
        print("update secret")
        return True