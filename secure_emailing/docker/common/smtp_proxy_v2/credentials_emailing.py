import psycopg2, psycopg2.extras, hashlib
from ConfigParser import SafeConfigParser
import logging

class StoreCredentials(object):
    def __init__(self):
        self.stored = False
        self.username = None
        self.password = None

    def data_pg(self, username, password):
        self.username = username
        self.password = password

        # Conf database
        parser = SafeConfigParser()
        parser.read('emailing.conf')
        self.db_name = parser.get('POSTGRES', 'db_name')
        self.db_user = parser.get('POSTGRES', 'db_user')
        self.db_passwd = parser.get('POSTGRES', 'db_passwd')
        self.db_host = parser.get('POSTGRES', 'db_host')

        hash_object = hashlib.md5(self.password)
        pass_user_external = hash_object.hexdigest()
        conn = psycopg2.connect(database=self.db_name ,user=self.db_user, password=self.db_passwd, host=self.db_host)
        cur = conn.cursor()
        cur.execute("SELECT id FROM emailing_users WHERE name='%s'" % self.username)
        id_user_internal = cur.fetchone()

        # Find user
        if id_user_internal == [] or id_user_internal == None:
            cur.close()
            conn.close()
            return False
        else:
            id_user_internal = id_user_internal[0]
            cur.execute("SELECT passwd FROM emailing_users WHERE id=%s" % id_user_internal)
            passwd_user_internal = cur.fetchone()[0]
            if pass_user_external == passwd_user_internal:
                cur.close()
                conn.close()
                self.id_user_internal = id_user_internal
                return id_user_internal
            else:
                cur.close()
                conn.close()
                return False

    def validate(self, username, password):
        self.username = username
        self.password = password

        data_pg_exit = self.data_pg(self.username, self.password)

        if data_pg_exit:
            return True
        else:
            return False

    def validate_mailfrom(self, mailfrom, username, password):
        self.username = username
        self.password = password

        domainfrom = mailfrom.split('@')
        domainfrom = domainfrom[1]

        data_pg_exit = self.data_pg(self.username, self.password)

        if data_pg_exit:
            parser = SafeConfigParser()
            parser.read('emailing.conf')
            self.db_name = parser.get('POSTGRES', 'db_name')
            self.db_user = parser.get('POSTGRES', 'db_user')
            self.db_passwd = parser.get('POSTGRES', 'db_passwd')
            self.db_host = parser.get('POSTGRES', 'db_host')

            hash_object = hashlib.md5(self.password)
            pass_user_external = hash_object.hexdigest()
            conn = psycopg2.connect(database=self.db_name ,user=self.db_user, password=self.db_passwd, host=self.db_host)
            
            cur = conn.cursor()
            cur.execute("""SELECT domain
                        FROM emailing_domains
                        WHERE id IN (SELECT id_domain
                                     FROM emailing_users_domains
                                     WHERE id_user = %s)""" % data_pg_exit)
            domains = cur.fetchall()

            cur.execute("""SELECT address
                            FROM emailing_addresses
                            WHERE id IN (SELECT id_address
                                     FROM emailing_users_addresses
                                     WHERE id_user = %s)""" % data_pg_exit)
            adress = cur.fetchall()
            cur.close()
            conn.close()

            allow_domain = False
            for d in domains:
                if d[0] == domainfrom:
                    allow_domain = True

            allow_mail = False
            for a in adress:
                if a[0] == mailfrom:
                    allow_mail = True

            if allow_mail or allow_domain:
                return True
            else:
                return False
        else:
            return False
