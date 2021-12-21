import requests
import pushy.util.localStorage as localStorage
from pushy.config import config

def getApiHost():
    # Development API endpoint for localhost
    # return config['api']['devEndpoint']
    
    # Attempt to fetch Pushy Enterprise hostname (may be null)
    enterpriseEndpoint = localStorage.get(config['storageKeys']['enterpriseEndpoint'])

    # Pushy Enterprise endpoint or fallback to Pushy Pro API endpoint
    return enterpriseEndpoint or config['api']['endpoint']

def post(path, json):
    # Build full URL to API endpoint
    url = getApiHost() + path

    # Execute HTTP request
    response = requests.post(url, json=json)

    # Invalid status code?
    if response.status_code < 200 or response.status_code > 299:
        # Convert response to JSON
        json = response.json()
        
        try:
            # Try extracting error code
            error = json['code'] + ': '
        except:
            error = ''

        try:
            # Try extracting error message
            error += json['error']
        except KeyError:
            error = 'An unknown error occurred'

        # Throw detailed error
        raise Exception(error + ' (HTTP status code ' + str(response.status_code) + ')')
    
    # Convert response to JSON and return it
    return response.json()