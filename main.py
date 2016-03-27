import database
from sys import stdout
from os import system, chmod, path
import stat
import configparser
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from fileReader import *

#Przechowuje sciezke, w ktorej bedziemy tworzyc nasza baze danych
#Przechowu sciezke do pliku, z ktorego bedziemy odczytywac informacje
dbname = None
fname = None

#Funkcja zapisujaca do pliku informacje bazie danych oraz o pliku z ktorego beda przetwarzane parametry do generowania
def config_ini_creator():
	config = configparser.ConfigParser()
	config.add_section('DATABASE')
	config.set('DATABASE', 'name', 'sqlite3')
	config.set('DATABASE', 'version', sqlite3.version)
	config.set('DATABASE', 'sqlite_version', str(sqlite3.sqlite_version))
	config.set('DATABASE', 'dbname', dbname)
	config.add_section('AIRPLANE LOGS')
	config.set('AIRPLANE LOGS', 'fileName', fname)
	with open('config.ini', 'w') as configfile:
		  config.write(configfile)

#Tworzenie bazy danych i utworzenie tabeli reprezentujacej czarna skrzynke
# - w przypadku istnienia pliku o podanej przez nas nazwie usuwa go i nadaje prawa
# - tworzy tabele AIRPLANE przechowujaca nasze rekordy
def database_creator():
	db = database.MyDB()
	chmod('clearDB.sh', stat.S_IRWXU)
	system('./clearDB.sh %s' % db.db_name)
	db.connect()

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
	del db
	
#Ustawiamy zmienna odpowiedzialna za przechowywanie sciezki do naszej bazy danych
def set_db_path():
	global dbname
	dbname = asksaveasfilename() + '.db'
	db_text.set(path.basename(path.normpath(dbname)))
	
#Ustawiamy zmienna odpowiedzialna za przechowywanie sciezki do pliku, z ktorego bedziemy generowac dane
def set_file_to_read():
	global fname
	fname = askopenfilename(filetypes=(("All files", "*.*"),))
	log_text.set(path.basename(path.normpath(fname)))
	
#Funkcja konfigurujaca nasze parametry i rozpoczyna symulacje lotu samolotu
def start_generate():
	config_ini_creator()
	database_creator()
	system('python3 generate.py')
	
#Funkcja odpowiedzialna za otworzenie programu do odczytywania danych
def open_black_box():
	system('python3 black_box.py')

if __name__ == "__main__":	
	#Tworzymy obiekt odpoweidzialny za nasze GUI i definiujemy jego podstawowe parametry
	root = Tk()
	root.style = ttk.Style()
	root.style.theme_use("clam")
	root.title("Fly recorder - configure")

	mainframe = ttk.Frame(root, padding="3 3 12 12")
	mainframe.grid(column=0, row=0)
	mainframe.columnconfigure(0, weight=1)
	
	db_text = StringVar()
	log_text = StringVar()
	ttk.Label(mainframe, text="Log file path").grid(column=1, row=1, pady=10, sticky=W+E)
	db_field = ttk.Entry(mainframe, textvariable=log_text, state='disabled')
	db_field.grid(column=2, row=1, pady=10)
	ttk.Label(mainframe, text="Database file path").grid(column=1, row=2, pady=10, sticky=W+E)
	log_field = ttk.Entry(mainframe, textvariable=db_text, state='disabled')
	log_field.grid(column=2, row=2, pady=10)
	
	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Import logs", command=set_file_to_read)
	filemenu.add_command(label="Save database", command=set_db_path)
	filemenu.add_command(label="Generate blackbox", command=start_generate)
	filemenu.add_command(label="Open blackbox", command=open_black_box)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="Option", menu=filemenu)

	#Ustawienie rozmiaru okna i jego blokada
	root.geometry('{}x{}'.format(300, 100))
	root.resizable(width=FALSE, height=FALSE)
	root.config(menu=menubar)
	#Dzialanie naszego GUI w petli
	root.mainloop()

	
	
	
	
