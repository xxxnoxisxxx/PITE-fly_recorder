import database
import logging
from sys import stdout
from os import system, chmod
import stat
import configparser
import sqlite3


try:
	''''logger = logging.getLogger('configure')
	logger.setLevel(logging.INFO)
	formatter = logging.Formatter('%(asctime)s - %(name)s - LINE: %(lineno)s - %(levelname)s - %(message)s')
	ch = logging.StreamHandler(stdout)
	ch.setFormatter(formatter)
	logger.addHandler(ch)'''

	#logger.info('Tworzenie pliku konfiguracyjnego!')
	config = configparser.ConfigParser()
	config.add_section('DATABASE')
	config.set('DATABASE', 'name', 'sqlite3')
	config.set('DATABASE', 'version', sqlite3.version)
	config.set('DATABASE', 'sqlite_version', str(sqlite3.sqlite_version))
	config.set('DATABASE', 'dbname', input("Podaj nazwe bazy danych.\n") + '.db')
	config.add_section('AIRPLANE LOGS')
	config.set('AIRPLANE LOGS', 'fileName', input("Podaj nazwe pliku do przetworzenia danych.\n"))
	with open('config.ini', 'w') as configfile:
		  config.write(configfile)

	#logger.info('Tworzenie bazy danych!')
	db = database.MyDB()
	chmod('clearDB.sh', stat.S_IRWXU)
	system('./clearDB.sh %s' % db.db_name)
	db.connect()

	#logger.info('Tworzenie tabel w bazie danych!')
	#logger.info('Tworzenie tabeli AIRPLANE.')
	query = '''CREATE TABLE "AIRPLANE" (
		"id" INTEGER PRIMARY KEY AUTOINCREMENT,
		"datetime" TEXT NOT NULL,
		"position_latitude" TEXT NOT NULL,
		"position_longitude" TEXT NOT NULL,
		"orientation_course" TEXT NOT NULL,
		"orientation_direction" TEXT NOT NULL,
		"groundspeed_kts" TEXT NOT NULL,
		"groundspeed_km_per_h" TEXT NOT NULL,
		"altitude_feet" TEXT NOT NULL,
		"rate" TEXT NOT NULL
	);'''
	db.query(query)

	#logger.info('Koniec tworzenia bazy danych.')

except Exception as err:
	print (err)
