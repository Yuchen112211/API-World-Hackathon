import json
from datetime import datetime
from datetime import timedelta  
import ActivitySeachAPIV2
from Algorithms import getWeatherFilterQuery
from zip_to_address_name import zip_to_address_name

ACTIVITY_API_KEY = "g83cs8mdp8shsmq5xeqvupzf"

def lambda_handler(event, context):
    today = datetime.today()

    zipcode = event["queryStringParameters"].get("zipcode", "")
    date = event["queryStringParameters"].get("date", today.strftime('%Y-%m-%d'))
    radius = event["queryStringParameters"].get("radius", 25)

    start_date = datetime.strptime(date, '%Y-%m-%d')
    some_days_later = start_date + timedelta(days=30)
    start_date_str = start_date.strftime('%Y-%m-%d') + ".." + some_days_later.strftime('%Y-%m-%d')
    
    city = zip_to_address_name(str(zipcode))
    
    current_weather, recommendated_categories = getWeatherFilterQuery(zipcode)
    activity_params = {
        "api_key": ACTIVITY_API_KEY,
        "radius": radius,
        "near": city,
        "start_date": start_date_str
    }
    activityApiInstance = ActivitySeachAPIV2.activityApi()
    all_activities = []
    for category in recommendated_categories:
        activity_params["query"] = category
        activityApiInstance.initialize_activity_information(activity_params)
        activities = activityApiInstance.form_all_info(50)
        all_activities.append(activities)
    result = {
        "activities": all_activities,
        "weather" : current_weather
    }
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
