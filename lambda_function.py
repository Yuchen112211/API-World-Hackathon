import json
from datetime import datetime
from datetime import timedelta  
import ActivitySeachAPIV2
from MeetupAPIV2 import MeetupAPI
from Algorithms import getWeatherFilterQuery
from zip_utils import zip_to_city_name, zip_to_lat_lon

ACTIVITY_API_KEY = "g83cs8mdp8shsmq5xeqvupzf"

def lambda_handler(event, context):
    today = datetime.today()

    zipcode = event["queryStringParameters"].get("zipcode", "")
    date = event["queryStringParameters"].get("date", today.strftime('%Y-%m-%d'))
    radius = event["queryStringParameters"].get("radius", 25)

    start_date = datetime.strptime(date, '%Y-%m-%d')
    some_days_later = start_date + timedelta(days=30)
    start_date_str = start_date.strftime('%Y-%m-%d') + ".." + some_days_later.strftime('%Y-%m-%d')
    
    city = zip_to_city_name(str(zipcode))
    lat_lon = zip_to_lat_lon(str(zipcode))

    current_weather, recommendated_categories = getWeatherFilterQuery(zipcode)
    activity_params = {
        "api_key": ACTIVITY_API_KEY,
        "radius": radius,
        "near": city,
        "start_date": start_date_str
    }
    activityApiInstance = ActivitySeachAPIV2.activityApi()

    meetup_params = {
        'lat': lat_lon['lat'],
        'lon': lat_lon['lng'],
        'radius': radius,
        'start_date_range': start_date.strftime('%Y-%m-%dT%H:%M:%S')
    }
    meetupClient = MeetupAPI()
   
    all_activities = []
    for category in recommendated_categories:
        activity_params["query"] = category['name']
        meetup_params["topic_category"] = category['id']
        activityApiInstance.initialize_activity_information(activity_params)
        activities = activityApiInstance.form_all_info(50)
        meetup_activities = meetupClient.find_events(meetup_params)
        print(meetup_activities)
        # parse the activities and meetup events and store in all activities
        all_activities.append(activities)
    result = {
        "activities": all_activities,
        "weather" : current_weather
    }
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
