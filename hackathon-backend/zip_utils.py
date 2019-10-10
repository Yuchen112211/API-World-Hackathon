import json
from botocore.vendored import requests

def zip_to_city_name(zip_code):
    zip_code = zip_code.strip()
    
    if zip_code == '':
        return {
            'statusCode': 400,
            'body': json.dumps('Resquest must contain the ZIP code.')
        }
        
    if not zip_code.isnumeric() or len(zip_code) != 5:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad format! The ZIP code should be a 5 digit number.')
        }
        
    
    geocoding_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    payload = {'address': zip_code, 'key': 'AIzaSyBfai_EdC2MTJ3OJl2AUBzhScAuV7CAp9Y'}
    
    response = requests.get(geocoding_url, params=payload)
    city_name = response.json()['results'][0]['formatted_address']
    
    return city_name
    
    
def zip_to_lat_lon(zip_code):
    zip_code = zip_code.strip()
    
    if zip_code == '':
        return {
            'statusCode': 400,
            'body': json.dumps('Resquest must contain the ZIP code.')
        }
        
    if not zip_code.isnumeric() or len(zip_code) != 5:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad format! The ZIP code should be a 5 digit number.')
        }
        
    
    geocoding_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    payload = {'address': zip_code, 'key': 'AIzaSyBfai_EdC2MTJ3OJl2AUBzhScAuV7CAp9Y'}
    
    response = requests.get(geocoding_url, params=payload)
    lat_lon = response.json()['results'][0]['geometry']['location']
    
    return lat_lon
    

if __name__ == "__main__":
    print(zip_to_city_name('10001'))
    print(zip_to_lat_lon('10001'))