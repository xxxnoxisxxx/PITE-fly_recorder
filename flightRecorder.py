#Klasa reprezentujaca nasz pomiar
# - czas pomiaru
# - szerokosc i dlugosc geograficzna
# - orientacje
# - wysokosc

class FlightRecorder(object):
	#Inicjalizacja parametrow klasy z przetworzonymi danymi z pliku
	def __init__(self, param):
		param = list(map(lambda x : x.strip(), param))
		self.datetime = param[0]
		self.position_latitude = param[1]
		self.position_longitude = param[2]
		self.orientation_course = param[3]
		self.orientation_direction = param[4]
		self.groundspeed_kts = param[5]
		self.groundspeed_km_per_h = param[6]
		self.altitude_feet = param[7]
		self.rate = param[8]
	#Zwraca informacje o zmiennych przechowywanych w klasie oraz ich wartosciach w postaci slownika
	def get_dict_params(self):
		return vars(self)
	#Zwraca informacje o zmiennych przechowywanych w klasie w postaci krotki
	def get_params(self):
		return (self.datetime, self.position_latitude, self.position_longitude, self.orientation_course, self.orientation_direction, self.groundspeed_kts, self.groundspeed_km_per_h + ' km/h', self.altitude_feet + ' ft', self.rate)
	#Zwraca sformatowanego przez nas stringa z informacjami		
	def get_info_short(self):
		inf = self.datetime +'\t\t\t' + self.position_latitude + '\t' + self.position_longitude + '\t\t' + self.orientation_course + '\t'
		inf += self.orientation_direction + '\t' + self.groundspeed_kts + '\t'
		inf += self.groundspeed_km_per_h + '\t' + self.altitude_feet + '\t' + self.rate
		return inf
		
