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
            self.db_connection = sqlite3.connect(self.db_name, isolation_level=None)
            self.db_cur = self.db_connection.cursor()
        except Exception as err:
            print(err)

    def query(self, query):
    	return self.db_cur.execute(query)
    	
    def insert_with_dict(self,params):
    	columns = ', '.join(params.keys())
    	placeholders = ':'+', :'.join(params.keys())
    	query = 'INSERT INTO AIRPLANE (%s) VALUES (%s)' % (columns, placeholders)
    	return self.db_cur.execute(query,params)
    	
    def clear(self):
    	self.db_cur.execute('DELETE FROM AIRPLANE WHERE id > 1')
		
    def __del__(self):
        self.db_connection.close()
    
