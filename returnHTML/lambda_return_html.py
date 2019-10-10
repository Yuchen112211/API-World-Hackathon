import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        "headers": {
            'Content-Type': 'text/html',
        },
        'body': '<html><head><title>HTML from API Gateway</title></head>' + 
        '<body><a href="https://secure.meetup.com/oauth2/authorize' +
        '?client_id=ppdp9n0tb1gtaa906d665b4g43&response_type=code&' +
        'redirect_uri=https://o2k881hv2k.execute-api.us-west-1.amazonaws.com/dev_stage/auth/redirect">Log in</a></body></html>'
    }
