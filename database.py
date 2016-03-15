import sqlite3
import configparser


class MyDB(object):
    db_connection = None
    db_cur = None
    db_name = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.db_name = config.get('DATABASE', 'dbname')

    def connect(self):
        try:
            self.db_connection = sqlite3.connect(self.db_name, isolation_level=None, check_same_thread=False)
            self.db_cur = self.db_connection.cursor()
        except Exception as err:
            print(err)

    def query(self, query, params=None):
        if params is not None:
            return self.db_cur.execute(query, params)
        else:
            return self.db_cur.execute(query)

    def __del__(self):
        self.db_connection.close()
