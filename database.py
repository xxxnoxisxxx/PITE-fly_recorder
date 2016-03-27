import sqlite3
import configparser

#Klasa reprezentujaca nasza baze danych
class MyDB(object):
	db_connection = None
	db_cur = None
	db_name = None
	#Ustawienie polaczenia z baza danych
	def __init__(self, name='default'):
		if name=='default':
			config = configparser.ConfigParser()
			config.read('config.ini')
			self.db_name = config.get('DATABASE', 'dbname')
		else:
			self.db_name = name
	#Nawiazanie polaczenia
	def connect(self):
		try:
			self.db_connection = sqlite3.connect(self.db_name, isolation_level=None)
			self.db_cur = self.db_connection.cursor()
		except Exception as err:
			print(err)
	#Wykonanie zapytania i zwrocenie wynikow
	def query(self, query):
		return self.db_cur.execute(query)
	#Dodawanie danych do bazy danych wykorzystujac slownik
	def insert_with_dict(self,params):
		columns = ', '.join(params.keys())
		placeholders = ':'+', :'.join(params.keys())
		query = 'INSERT INTO AIRPLANE (%s) VALUES (%s)' % (columns, placeholders)
		return self.db_cur.execute(query,params)
	#Czyszczenie rekordow w bazie danych
	def clear(self):
		self.db_cur.execute('DELETE FROM AIRPLANE WHERE id > 1')
	#Konczenie polaczenia z baza danych
	def __del__(self):
		self.db_connection.close()
    
