from botocore.vendored import requests
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('access_token')

class MeetupAPI:
    """
    Meetup API Client
    """

    def __init__(self, userId="1"):
        response = table.get_item(
            Key={'id': userId}
        )
        self.access_token = response['Item']['access_token']
        self.url = 'https://api.meetup.com/find/upcoming_events'
    
    def find_events(self, params):
        headers = {
            'Authorization': 'Bearer ' + self.access_token
        }
        response = requests.get(url=self.url, params=params, headers=headers)
        r = response.json()
        return r['events']