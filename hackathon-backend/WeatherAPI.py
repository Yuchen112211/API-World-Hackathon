import boto3
import json

from botocore.exceptions import ClientError
from botocore.vendored import requests


# Wrap the func with try & except. 
# Catches of wrong city name error.
def city_name_might_not_exist(func):
	def wrapper(*args, **kwargs):
		try:
			ret_val = func(*args, **kwargs)
			return ret_val
		except ClientError as e:
			return "Error - City Name dose not exist!"

	return wrapper

def current_data_none(func):
	def wrapper(*args, **kwargs):
		try:
			ret_val = func(*args, **kwargs)
			return ret_val
		except KeyError as e:
			return "Error - data does not exists or formated before."

	return wrapper

class weatherApi:
	"""
	This is the helper class of Weather API.
	"""

	def __init__(self):
		self.weather_url = "http://api.openweathermap.org/data/2.5/forecast?"
		self.data = {}

	#Get the id of the given city name.
	#Won't be called by clients.
	@city_name_might_not_exist
	def get_place(self, city_name):
		db = boto3.resource("dynamodb", "us-east-2")
		table = db.Table("us-cities")
		keys = {"name":city_name}
		return DynamodbConnect.get_data(table, keys)

	#Form the weather data to the form we want.
	#Won't be called by clients.
	@current_data_none
	def form_data(self):
		result_data = []
		for i in self.data:
			tmp = {}
			tmp['date'] = i['dt_txt']
			tmp['weather'] = i['weather'][0]['main']
			tmp['weather_description'] = i['weather'][0]['description']
			tmp['wind_speed'] = i['wind']['speed']
			tmp['highest_temperature'] = i['main']['temp_max'] - 273.15 
			tmp['lowest_temperature'] = i['main']['temp_min'] - 273.15 
			tmp['humidity'] = i['main']['humidity']

			result_data.append(tmp)

		self.data = result_data

	#Get the weather information based on the given city name.
	#This will be called by clients.
	@city_name_might_not_exist
	def get_place_weather_city_name(self, city_name):
		raw_place = self.get_place(city_name)
		if raw_place['error'] != "None":
			return raw_place['error']

		city_id = int(raw_place['id'])
		api_key = ""
		weather_url = self.weather_url + "id=" + str(city_id) +"&APPID=" + api_key
		r = requests.get(weather_url)
		self.data = r.json()['list']
		self.form_data()

	#Get the weather information based on the given zipcode.
	#This will be called by clients.
	@city_name_might_not_exist
	def get_place_weather_zipcode(self, zipcode):

		zipcode = int(zipcode)
		api_key = "970bf7797937283622e2bc3301d07f06"
		weather_url = self.weather_url + "zip=" + str(zipcode) +",us&APPID=" + api_key
		r = requests.get(weather_url)
		self.data = r.json()['list']
		self.form_data()
		
	#Get the average tmperature
	#Return two dictionary
	def get_average_tmperature(self):
		average_highest_temp = {}
		average_lowest_temp = {}

		for i in self.data:
			date_now = i['date'].split(' ')[0]
			if date_now not in average_highest_temp:
				average_highest_temp[date_now] = [i['highest_temperature']]
				average_lowest_temp[date_now] = [i['lowest_temperature']]
			else:
				average_highest_temp[date_now].append(i['highest_temperature'])
				average_lowest_temp[date_now].append(i['lowest_temperature'])
		for i in average_lowest_temp:
			average_highest_temp[i] = sum(average_highest_temp[i]) / len(average_highest_temp[i])
			average_lowest_temp[i] = sum(average_lowest_temp[i]) / len(average_lowest_temp[i])
		return average_lowest_temp,average_highest_temp			

	#Get main weather of the day.
	#Use the collections package. Not sure how to use it in lambda.
	def get_main_weather(self):
		import collections
		main_weather = {}
		for i in self.data:
			date_now = i['date'].split(' ')[0]
			if date_now not in main_weather:
				main_weather[date_now] = [i['weather']]
			else:
				main_weather[date_now].append(i['weather'])
		for i in main_weather:
			main_weather[i] = collections.Counter(main_weather[i]).most_common(1)[0][0]
		return main_weather
