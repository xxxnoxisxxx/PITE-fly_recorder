from flightRecorder import *
import configparser

class FileReader(object):
	def __init__(self):
		self.data = []
		config = configparser.ConfigParser()
		config.read('config.ini')
		self.fileName = config.get('AIRPLANE LOGS', 'fileName')
	def read(self):
		with open(self.fileName) as file:
			lines = file.read().splitlines()
		for line in lines:
			self.data.append(FlightRecorder(line.split('\t')))
	def get_data(self):
		return self.data
