from botocore.vendored import requests
import json
import decimal
import boto3

# Wrap the func with try & except. 
# Catches of index error, but still informs callers.
def index_may_out_of_range(func):
	def wrapper(*args, **kwargs):
		try:
			ret_val = func(*args, **kwargs)
			return ret_val
		except IndexError:
			return "Warning - No available activity!"

	return wrapper

class activityApi:
	"""
	activityApi is the helper class for 'ACTIVITY SEARCH API V2'.
	
	Start by calling initialize_activity_information, which is going to 
	send the GET request and save the response into self.data.
	"""
	def __init__(self):
		self.weather_url = "http://api.amp.active.com/v2/search"
		self.data = {}


	#Get all the data from the params that the user provide.
	#Store them into self.data as a dictionary.
	def initialize_activity_information(self, params):
		r = requests.get(url = self.weather_url, params = params)
		self.data = r.json()

	def get_result_cnt(self):
		if self.data:
			return int(self.data['total_results'])
		else:
			return 0

	#Get the activity's place. index indicates the offset in the whole result.
	@index_may_out_of_range
	def get_place(self, index):
		current_data = self.data["results"][index]['place']
		want_keys = ["postalCode", "countryCode", "cityName", "stateProvinceCode", "timezone"]
		return {i:current_data[i] for i in want_keys}

	#Get the start date and the end date.
	#All in dddd-mm-yyyy forms.
	@index_may_out_of_range
	def get_date(self, index):
		current_data = self.data["results"][index]
		want_keys = ['salesStartDate','salesEndDate','activityStartDate','activityEndDate','createdDate']
		return {i:current_data[i] for i in want_keys}

	#Get the name of the activity/asset as a String
	@index_may_out_of_range
	def get_name(self, index):
		return self.data["results"][index]['assetName']

	#Get the related topic of the activity. The method would return all topics.
	#Every list element, as a dictionary, would contains:
	#topicId,topicName and topicTaxonomy(I do not know what this means).
	@index_may_out_of_range
	def get_topics(self, index):
		topics = [i['topic'] for i in self.data["results"][index]['assetTopics']]
		return topics

	#Get the related category of the activity.
	#Contains: categoryTaxonomy(again,IDK), categoryName and categeoryId.
	@index_may_out_of_range
	def get_categories(self, index):
		categories = [i['category'] for i in self.data["results"][index]["assetCategories"]]
		return categories

	#Get the related channels of the activity.
	#Contains: channelName,channelDsc(description) and channelId.
	@index_may_out_of_range
	def get_channels(self, index):
		channels = [i['channel'] for i in self.data["results"][index]["assetChannels"]]
		return channels

	#Get the description of the activity.
	#Get all the descriptions. Need html parsing later.
	@index_may_out_of_range
	def get_descriptions(self, index):
		return [i['description'] for i in self.data["results"][index]["assetDescriptions"]]

	#Get all the tags of the activity.
	#Contains: tagDescription,tagName. Each activity has multiple descriptions.
	@index_may_out_of_range
	def get_tags(self, index):
		return [{'tagDescription':i['tag']['tagDescription'], 'tagName':i['tag']['tagName']} for i in self.data["results"][index]["assetTags"]]

	#Get the related organization of the activity.
	@index_may_out_of_range
	def get_organization(self, index):
		current_data = self.data["results"][index]['organization']
		want_keys = ["organizationName","addressPostalCd","addressCityName","addressStateProvinceCode"]
		return {i:current_data[i] for i in want_keys}

	#Get the status of the activity.
	@index_may_out_of_range
	def get_sales_status(self, index):
		return self.data["results"][index]['salesStatus'] 

	@index_may_out_of_range
	def determineDuplicate(self,results,key):
		if type(results[key]) == type({}):
			for i in results[key]:
				results[i] = results[key][i]
			results.pop(key)
		elif type(results[key]) == type([]):
			for i in results[key][0]:
				results[i] = results[key][0][i]
			results.pop(key)

	@index_may_out_of_range
	def get_all_info(self,index):
		results = {}

		results['place'] = self.get_place(index)
		self.determineDuplicate(results,'place')

		results['date'] = self.get_date(index)
		self.determineDuplicate(results,'date')

		results['name'] = self.get_name(index)
		self.determineDuplicate(results,'name')

		results['topics'] = self.get_topics(index)
		self.determineDuplicate(results,'topics')

		results['categories'] = self.get_categories(index)
		self.determineDuplicate(results,'categories')

		results['tags'] = self.get_tags(index)
		self.determineDuplicate(results,'tags')

		results['organization'] = self.get_organization(index)
		self.determineDuplicate(results,'organization')

		results['status'] = self.get_sales_status(index)
		self.determineDuplicate(results,'status')

		results['resource'] = "Access"
		return results

	@index_may_out_of_range
	def form_all_info(self,num):
		length = self.get_result_cnt()
		result = []
		for i in range(min(length,num)):
			result.append(self.get_all_info(i))
		return result