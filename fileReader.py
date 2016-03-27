from flightRecorder import *
import configparser

#Klasa odpowiedzialna za wczytanie danych do symulowania lotu
class FileReader(object):
	#Pobranie nazwy pliku z plikiem do symulowania danych
	def __init__(self):
		self.data = []
		config = configparser.ConfigParser()
		config.read('config.ini')
		self.fileName = config.get('AIRPLANE LOGS', 'fileName')
	#Odczytywanie i wstepne przetworzenie danych
	def read(self):
		with open(self.fileName) as file:
			lines = file.read().splitlines()
		for line in lines:
			self.data.append(FlightRecorder(line.split('\t')))
	#Zwraca liste z naszymi rekordami
	def get_data(self):
		return self.data

