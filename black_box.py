from fileReader import *
from databaseParser import *
import time
import database
from datetime import datetime
from enum import Enum
import csv

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import asksaveasfilename

import random
import tkinter.scrolledtext as ScrolledText
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.dates as mdate

#Definiujemy obiekt do rysowania wykresow		
f = Figure(figsize=(15,5), dpi=50)
#Definiujemy wykresy
a = f.add_subplot(111)
#Przechowuje czas rekordu
time_list = []
#Przechowuje wysokosc samolotu
altitude_list = []
#Przechowuje szybkosc samolotu w wezlach
kts_list = []
#Przechowuje szybkosc samolotu w km/h
speed_list = []

#Klasa przechowujaca typy wykresu
class ChartType(Enum):
	ALTITUDE, SPEED, KTS = range(3)
#Zmienna przechowujaca aktualny typ wykresu
actual_chart_type = ChartType.ALTITUDE.value
#Funkcja zwracajaca parametry do wyswietlenia wykresu w zaleznosci od wybranego typu
def choose_type(argument):
	switcher = {
  						0: ('Altitude ft', altitude_list, 'RED'),
        			1: ('Speed km/h', speed_list, 'BLUE'),
        			2: ('KTS', kts_list, 'GREEN'),
   }
	return switcher.get(argument)

def change_type(chart_type):
	global actual_chart_type
	actual_chart_type = chart_type

#Funkcja nawiazujaca polaczenie z nasza baza danych
def db_init():
	global db
	db = database.MyDB()
	db.connect()

#Funkcja ladujaca odpowiednia baze danych
# - wybieramy nasza baze danych do odczytu
# - formatujemy odpowiednio nasze dane
# - odczytujemy dane i inicjalizujemy pola w naszym GUI
def load_data():
	global fname
	fname = askopenfilename(filetypes=(("Database", "*.db"),))
	
	#Czyszczenei danych i wykresu
	clear_log()
	clear_charts_params()
	
	res = db.query('SELECT * from AIRPLANE')
	global records
	records = DatabaseParser.parse_data(res.fetchall())
	
	print_log_header()
	for record in records:
		print_log(record.get_info_short())
		
	prepare_charts_data(records)
	#draw_charts()
	#print_log()


def print_log_header():
	txt2.configure(state="normal")
	txt2.insert(INSERT, 'Datetime\t\t\tLat.\tLong.\t\tCour.\tDir.\tKTS\tKM\h\tAlt.\tRate')
	txt2.see(END)
	txt2.configure(state="disabled")

def print_log(record):
	txt.configure(state="normal")
	txt.insert(INSERT, str(record) + '\n')
	txt.see(END)
	txt.configure(state="disabled")
	
def convert_data(str_date):
	return time.mktime(datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S").timetuple())
	
def prepare_charts_data(records):
	for record in records:
		time_list.append(convert_data(record.datetime))
		altitude_list.append(record.altitude_feet.replace(',',''))
		kts_list.append(record.groundspeed_kts)
		speed_list.append(record.groundspeed_km_per_h)
	
def draw_charts(i):
	a.clear()
	#Formatowanie wykresu
	secs = mdate.epoch2num(time_list)
	date_fmt = '%d-%m-%y %H:%M:%S'
	date_formatter = mdate.DateFormatter(date_fmt)
	a.xaxis.set_major_formatter(date_formatter)
	f.autofmt_xdate()
	#Pobranie typu i informacji o nim
	chart_type = choose_type(actual_chart_type) 
	#Ustawienia etykiet
	a.set_ylabel(chart_type[0], color=chart_type[2])
	#Rysowanie wykresow
	a.plot_date(secs,chart_type[1], linestyle='-', color=chart_type[2])
	
def clear_log():
	txt.configure(state="normal")
	txt.delete('0.0', END)
	txt.configure(state="disabled")
	
def clear_charts_params():
	time_list[:] = []
	altitude_list[:] = []
	kts_list[:] = []
	speed_list[:] = []
	
def save_chart():
	filename = asksaveasfile(mode='w', defaultextension=".png")
	a.get_figure().savefig(filename)
	
def save_csv():
	filename = asksaveasfilename()
	with open(filename+'.csv', "w") as f:
		writer = csv.writer(f, delimiter=";")
		writer.writerow(['Datetime', 'Position Latitude', 'Position Longtitude', 'Orientation Course', 'Orientation Direction', 'Groundspeed KTS', 'Groundspeed KM\H', 'Altitude feet', 'Rate'])
		for row in records:
			writer.writerow(row.get_params())

if __name__ == "__main__":
	#Nawiazanie polaczenia z baza danych
	db_init()
	
	#Tworzymy obiekt odpoweidzialny za nasze GUI i definiujemy jego podstawowe parametry
	root = Tk()
	root.style = ttk.Style()
	root.style.theme_use("clam")
	root.title("Fly recorder - black box")

	mainframe = ttk.Frame(root, padding="3 3 12 12")
	mainframe.grid(column=0, row=0)
	mainframe.columnconfigure(0, weight=1)
	
	#Definiujemy i konfigurujemy pasek menu
	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Open", command=load_data)
	filemenu.add_command(label="Save chart as...", command=save_chart)
	filemenu.add_command(label="Export to CSV", command=save_csv)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="File", menu=filemenu)
	
	editmenu = Menu(menubar, tearoff=0)
	editmenu.add_command(label="Atitude", command=lambda: change_type(ChartType.ALTITUDE.value))
	editmenu.add_command(label="Speed", command=lambda: change_type(ChartType.SPEED.value))
	editmenu.add_command(label="KTS", command=lambda: change_type(ChartType.KTS.value))
	menubar.add_cascade(label="Chart", menu=editmenu)
	
	#Zmieniamy ulozenie elementow
	for child in mainframe.winfo_children(): child.grid_configure(padx=10, pady=10)

	#Definiujemy obszar na ktorym bedzie rysowany wykres
	canvas = FigureCanvasTkAgg(f,mainframe)
	canvas.show()
	canvas.get_tk_widget().grid(column=1, row=1, padx=15)
	canvas._tkcanvas.grid(column = 1, row=1)

	#Definiujemy obszar, ktory bedzie wyswietlal wygenerowane parametry
	txt = ScrolledText.ScrolledText(mainframe, height = 9, state="normal")
	txt.grid(column=1,row=4, columnspan=3, sticky=(E,W))
	txt2 = ScrolledText.ScrolledText(mainframe, height = 1, state="normal")
	txt2.grid(column=1,row=3, columnspan=3, sticky=(E,W), pady=10)

	ani = animation.FuncAnimation(f, draw_charts, interval=1000)
	#Ustawienie paska narzędzi, rozmiaru okna i jego blokady
	root.config(menu=menubar)
	root.geometry('{}x{}'.format(800, 600))
	root.resizable(width=FALSE, height=FALSE)

	#Dzialanie naszego GUI w petli
	root.mainloop()
