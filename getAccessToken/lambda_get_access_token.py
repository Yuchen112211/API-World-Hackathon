import json
import boto3
from botocore.vendored import requests


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('access_token')

def lambda_handler(event, context):
    code = event["queryStringParameters"].get("code", "")
    state = event["queryStringParameters"].get("state", "")
    error = event["queryStringParameters"].get("error", "")
    
    userId = "1"
    
    if error:
        return {
        'statusCode': 401,
        'body': json.dumps(error)
    }
    
    # Get access token using authorization code
    data = {
        'client_id': 'ppdp9n0tb1gtaa906d665b4g43',
        'client_secret': 'g8fduoqsshtq4fgf8i4vegcdab',
        'grant_type': 'authorization_code',
        'redirect_uri': 'https://o2k881hv2k.execute-api.us-west-1.amazonaws.com/dev_stage/auth/redirect',
        'code': code
    }
    
    oauth_url = "https://secure.meetup.com/oauth2/access"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    
    response = requests.post(oauth_url, data=data, headers=headers)
    item = response.json()
    
    
    if response.status_code != 200:
        return {
            'statusCode': 200,
            'body': json.dumps(item['error'])
        }
        
    # Save access token into database
    item['id'] = userId
    response = table.put_item(Item={
            'id': item['id'],
            'access_token': item['access_token'],
            'refresh_token': item['refresh_token']
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            "code": code,
            "access_token": item["access_token"]
        })
    }
