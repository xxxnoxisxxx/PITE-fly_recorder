import time
from datetime import datetime

from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as ScrolledText
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.dates as mdate

from fileReader import *
import database

#Flaga sprawdzajaca czy dalej wczytujemy dane
change_data= True
#Przechowuje czas rekordu
time_list = []
#Przechowuje wysokosc samolotu
altitude_list = []
#Przechowuje szybkosc samolotu w wezlach
kts_list = []
#Definiujemy obiekt do rysowania wykresow		
f = Figure(figsize=(7,5), dpi=59)
#Definiujemy wykresy
a_altitude = f.add_subplot(111)
a_speed = a_altitude.twinx()
#Zmienna przechowujaca pole tekstowe, w ktorym beda znajdowac sie nasze aktualnie wygenerowane logi
txt = None
#Zmienna przechowujaca wartosci naszych aktualnych parametrow
text_variable_list = None
#Zmienna przechowujaca obiekt naszej bazy
db = None
#Zmienna przechowujaca nasz iterator do pobranych danych z pliku
it = None

#Funkcja nawiazujaca polaczenie z nasza baza danych i czyszczcaca poprzednie rekordy
def db_init():
	global db
	db = database.MyDB()
	db.connect()
	db.clear()

#Funkcja pobierajaca nasze dane z pliku
def get_data_from_file():
	#Pobieramy odczytane z pliku dane do generowania i przetwarzamy je wstepnie
	flight = FileReader()
	flight.read()
	data = flight.get_data()
	#Tworzenie iteratora do generowanych danych
	global it
	it = iter(data) 

#Funkcja aktualizujaca log
def print_data(record):
		txt.configure(state="normal")
		txt.insert(INSERT, record.get_info_short() + '\n')
		txt.see(END)
		txt.configure(state="disabled")
		
#Funkcja konwerujaca nasza date
def convert_data(str_date):
	return time.mktime(datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S").timetuple())

#Funkcja aktualizujaca nasz wykresow
def draw_charts():
	#Czyszczenie wykresow
	a_altitude.clear()
	a_speed.clear()
	#Ustawienia zwiazane z wyswietlaniem czasu na osi OX
	secs = mdate.epoch2num(time_list)
	date_fmt = '%d-%m-%y %H:%M:%S'
	date_formatter = mdate.DateFormatter(date_fmt)
	a_altitude.xaxis.set_major_formatter(date_formatter)
	a_speed.xaxis.set_major_formatter(date_formatter)
	f.autofmt_xdate()
	#Ustawienia etykiet
	a_altitude.set_ylabel('Altitude [ft]', color='RED')
	a_speed.set_ylabel('KTS', color='GREEN')
	#Rysowanie wykresow
	a_altitude.plot_date(secs,altitude_list, linestyle='-', color='RED')
	a_speed.plot_date(secs, kts_list, linestyle='-', color='GREEN')

#Funkcja do aktualizowania aktualnych parametrow samolotu
def update_entry_fields(record_params):
	for i in range(len(text_variable_list)):
		text_variable_list[i].set(record_params[i])
		
#Funkcja przygotowujaca parametry do wyswietlenia na wykresie
def prepare_lists_to_plot(record_dict_params):
	altitude_list.append(record_dict_params['altitude_feet'].replace(',',''))
	kts_list.append(record_dict_params['groundspeed_kts'])
	time_list.append(convert_data(record_dict_params['datetime']))

		
#Funkcja symulator lotu na podstawie parametrow z pliku
# - iterujemy po pobranych danych z pliku
# - aktualizujemy nasze pola aktualnie pobranym parametrem
# - dodajemy do wyswietlanego logu nasz rekord z parametrami
#	- rysujemy wykres na podstawie aktualnie pobranych parametrow
# - zapisujemy aktualne parametry w bazie danych - 'czarnej skrzynce'
def animate(i):
	global change_data
	if change_data == True:
		try:
				#Iterujemy po obiekcie
				record = next(it)
				#Pobieramy parametry
				record_params = record.get_params()
				record_dict_params = record.get_dict_params()
				#Zmieniamy wartosci naszych pol wyswietlajacych aktualne parametry
				update_entry_fields(record_params)
				#Historia wyswietlen parametrow
				print_data(record)
				#Przygotowujemy listy danych do rysowania wykresow
				prepare_lists_to_plot(record_dict_params)
				#Rysujemy nasz wykresow
				draw_charts()
				#Zapisujemy do bazy nasz rekord
				db.insert_with_dict(record_dict_params)
		except StopIteration:
			change_data = False

if __name__ == "__main__":
	#Nawiazanie polaczenia z baza danych
	db_init()
	
	#Pobranie danych z pliku
	get_data_from_file()
	
	#Tworzymy obiekt odpoweidzialny za nasze GUI i definiujemy jego podstawowe parametry
	root = Tk()
	root.style = ttk.Style()
	root.style.theme_use("clam")
	root.title("Fly recorder - simulator")

	mainframe = ttk.Frame(root, padding="3 3 12 12")
	mainframe.grid(column=0, row=0)
	mainframe.columnconfigure(0, weight=1)

	#Definicja etykiet i pol w naszym GUI
	ttk.Label(mainframe, text="Datetime").grid(column=1, row=1, sticky=(N,E,W))
	e_date = ttk.Entry(mainframe)
	e_date.grid(column=2, row=1, sticky=(N,E,W))
	ttk.Label(mainframe, text="Latitude").grid(column=1, row=2, sticky=(W,E,N))
	e_lat = ttk.Entry(mainframe)
	e_lat.grid(column=2, row=2, sticky=(W,E,N))
	ttk.Label(mainframe, text="Longitude").grid(column=1, row=3, sticky=(W,E,N))
	e_long = ttk.Entry(mainframe)
	e_long.grid(column=2, row=3, sticky=(W,E,N))
	ttk.Label(mainframe, text="Course").grid(column=1,row=4, sticky=(W,E,N))
	e_course = ttk.Entry(mainframe)
	e_course.grid(column=2, row=4, sticky=(W,E,N))
	ttk.Label(mainframe, text="Direction").grid(column=1,row=5, sticky=(W,E,N))
	e_dir = ttk.Entry(mainframe)
	e_dir.grid(column=2, row=5, sticky=(W,E,N))
	ttk.Label(mainframe, text="KTS").grid(column=1,row=6, sticky=(W,E,N))
	e_speed = ttk.Entry(mainframe)
	e_speed.grid(column=2, row=6, sticky=(W,E,N))
	ttk.Label(mainframe, text="Speed").grid(column=1,row=7, sticky=(W,E,N))
	e_kts = ttk.Entry(mainframe)
	e_kts.grid(column=2, row=7, sticky=(W,E,N))
	ttk.Label(mainframe, text="Altitude").grid(column=1,row=8, sticky=(W,E,N))
	e_alti = ttk.Entry(mainframe)
	e_alti.grid(column=2, row=8, sticky=(W,E,N))
	ttk.Label(mainframe, text="Rate").grid(column=1,row=9, sticky=(W,E,N))
	e_rate = ttk.Entry(mainframe)
	e_rate.grid(column=2, row=9, sticky=(W,E,N))

	#Zmienna przechowujaca wartosci naszych parametrow lotu wyswietlane w danej chwili
	entry_list = [e_date, e_lat, e_long, e_course, e_dir, e_speed, e_kts, e_alti, e_rate]
	
	#Tworzenie zmiennych tekstowych przechowujacych aktualne parametry
	text_variable_list = [StringVar() for i in range(len(entry_list))]
	
	#Konfiguracja naszych pol przechowujacych zmienne tekstowe
	for i in range(len(entry_list)):
		entry_list[i].configure(textvariable=text_variable_list[i], state='disabled')	
	
	#Zmieniamy ulozenie elementow
	for child in mainframe.winfo_children(): child.grid_configure(padx=10, pady=10)

	#Definiujemy obszar na ktorym bedzie rysowany wykres
	canvas = FigureCanvasTkAgg(f,mainframe)
	canvas.show()
	canvas.get_tk_widget().grid(column=3, row=1, columnspan=7, rowspan=7, padx=50)
	canvas._tkcanvas.grid(column = 3, row=1)

	#Definiujemy obszar, ktory bedzie wyswietlal wygenerowane parametry
	txt = ScrolledText.ScrolledText(mainframe, height = 13, state="disabled")
	txt.grid(column=1,row=13, columnspan=9, sticky=(N,E,W))

	#Ustawiamy wykonanie naszej funkcji 'generatora danych'		
	ani = animation.FuncAnimation(f, animate, interval=500)

	#Ustawienie rozmiaru okna i jego blokada
	root.geometry('{}x{}'.format(800, 600))
	root.resizable(width=FALSE, height=FALSE)

	#Dzialanie naszego GUI w petli
	root.mainloop()
