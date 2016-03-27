from fileReader import *
from flightRecorder import *

#Klasa pobierajaca rekordy z bazy danych i przetwarzajaca je
class DatabaseParser(object):
	@staticmethod
	def parse_data(data):
		record_list = []
		for row in data:
			record_list.append(FlightRecorder(row[1:]))
		return record_list
