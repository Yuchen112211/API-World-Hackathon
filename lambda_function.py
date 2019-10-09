import json
from datetime import datetime
from datetime import timedelta  
import ActivitySeachAPIV2
from Algorithms import getWeatherFilterQuery


ACTIVITY_API_KEY = "g83cs8mdp8shsmq5xeqvupzf"

def lambda_handler(event, context):
    today = datetime.today()

    zipcode = event["queryStringParameters"].get("zipcode", "")
    date = event["queryStringParameters"].get("date", today.strftime('%Y-%m-%d'))
    radius = event["queryStringParameters"].get("radius", 25)

    start_date = datetime.strptime(date, '%Y-%m-%d')
    five_days_later = start_date + timedelta(days=10)
    start_date_str = start_date.strftime('%Y-%m-%d') + ".." + five_days_later.strftime('%Y-%m-%d')
    
    current_weather, query = getWeatherFilterQuery(zipcode)
    print(query)
    activity_params = {
        "api_key": ACTIVITY_API_KEY,
        "radius": radius,
        "zip": zipcode,
        "query": query,
        "start_date": start_date_str
    }
    activityApiInstance = ActivitySeachAPIV2.activityApi()
    activityApiInstance.initialize_activity_information(activity_params)
    all_activities = activityApiInstance.form_all_info(50)
    result = {
        "activities": all_activities,
        "weather" : current_weather
    }
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
