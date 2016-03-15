import database
import logging
from sys import stdout
from os import system, chmod
import stat
import configparser
import sqlite3

logger = logging.getLogger('configure')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - LINE: %(lineno)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler(stdout)
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.info('Tworzenie pliku konfiguracyjnego!')
config = configparser.ConfigParser()
config.add_section('DATABASE')
config.set('DATABASE', 'name', 'sqlite3')
config.set('DATABASE', 'version', sqlite3.version)
config.set('DATABASE', 'sqlite_version', str(sqlite3.sqlite_version))
config.set('DATABASE', 'dbname', input("Podaj nazwe bazy danych.\n"))
#config.set('DATABASE', 'user', input("Podaj nazwe uzytkownika.\n"))
#config.set('DATABASE', 'password', input("Podaj haslo.\n"))
with open('config.ini', 'w') as configfile:
    config.write(configfile)

logger.info('Tworzenie bazy danych!')
db = database.MyDB()
chmod('clearDB.sh', stat.S_IRWXU)
system('./clearDB.sh %s' % db.db_name)
db.connect()

logger.info('Tworzenie tabel w bazie danych!')
logger.info('Tworzenie tabeli AIRPLANE.')
query = '''CREATE TABLE "AIRPLANE" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "Name" TEXT NOT NULL,
  "StartLocation" TEXT NOT NULL,
  "EndLocation" TEXT NOT NULL,
  "Fuel" REAL NOT NULL,
  "High" REAL NOT NULL,
  "Speed" REAL NOT NULL,
  "Distance" REAL NOT NULL
);'''
db.query(query)

#logger.info('Dodawanie podstawowych rekordow.')
#query = 'INSERT INTO AIRPLANE VALUES(null,?,?,?,?,?,?,?)'
#db.query(query, ('AIRPLANE ONE', 'Krakow', 'London', 10000, 1000, 60, 2000))


logger.info('Koniec tworzenia bazy danych.')
