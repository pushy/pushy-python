import pushy.lib.api as api
import pushy.lib.mqtt as mqtt
from pushy.util.config import config
import pushy.util.localStorage as localStorage

def listen():
    # Connect to MQTT endpoint
    mqtt.connect()

def isRegistered():
    # Attempt to fetch existing token and auth
    token = localStorage.get(config['storageKeys']['token'])
    tokenAuth = localStorage.get(config['storageKeys']['tokenAuth'])
    
    # Both values must exist
    return token and tokenAuth

def validateDeviceCredentials():
    # Attempt to fetch existing token and auth
    token = localStorage.get(config['storageKeys']['token'])
    tokenAuth = localStorage.get(config['storageKeys']['tokenAuth'])

    # Not registered yet?
    if not token or not tokenAuth:
        raise Exception('The device is not registered to receive push notifications.')

    # JSON post data
    postData = { 
        'token': token, 
        'auth': tokenAuth,
        'sdk': int(config['sdk']['version'])
    }

    try:
        # Authenticate the device
        response = api.post('/devices/auth', postData)
    except Exception as e:
        # Request failed
        raise Exception('The API request failed: ' + str(e))

    # Validate response
    if not response['success']:
        raise Exception('An unexpected response was received from the Pushy API.')

def register(options):
    # Make sure options is an object
    if not options or type(options) is not dict:
        options = {}

    # No App ID passed in via options?
    if not options['appId']:
        raise Exception('Please provide your Pushy App ID as per the documentation.')

    # Attempt to fetch existing token and auth
    token = localStorage.get(config['storageKeys']['token'])
    tokenAuth = localStorage.get(config['storageKeys']['tokenAuth'])
    tokenAppId = localStorage.get(config['storageKeys']['tokenAppId'])

    # Check for new app ID different than the one we registered with
    if token and tokenAppId and options['appId'] and type(tokenAppId) is str and tokenAppId != options['appId']:
        token = None

    # Already registered?
    if token and tokenAuth:
        try:
            # Validate device credentials
            validateDeviceCredentials()

            # Attempt to connect
            mqtt.connect()

            # Device credentials are valid
            return token
        except Exception as e:
            # Ignore error and register new device
            print('Device validation error: ' + str(e))

    # JSON post data
    postData = {
        'appId': options['appId'],
        'sdk': int(config['sdk']['version']),
        'platform': config['sdk']['platform']
    }

    try:
        # Register the device
        response = api.post('/register', postData)
    except Exception as e:
        # Registration failed
        raise Exception('The API request failed: ' + str(e))

    # Validate response
    if not response['token'] or not response['auth']:
        raise Exception('An unexpected response was received from the Pushy API.')

    # Save device token and auth in local storage
    localStorage.set(config['storageKeys']['token'], response['token'])
    localStorage.set(config['storageKeys']['tokenAuth'], response['auth'])
    localStorage.set(config['storageKeys']['tokenAppId'], options['appId'])

    # Disconnect any existing connection
    mqtt.disconnect()

    # Start listening for notifications
    listen()

    # Provide app with device token
    return response['token']

def setNotificationListener(listener):
    # Store reference to listener
    mqtt.setNotificationListener(listener)
    
def setConnectionListener(listener):
    # Store reference to listener
    mqtt.setConnectionListener(listener)

def setDisconnectionListener(listener):
    # Store reference to listener
    mqtt.setDisconnectionListener(listener)

def loop_forever():
    # Avoid program termination
    mqtt.loop_forever()

def subscribe(topics):
    # Attempt to fetch existing token and auth
    token = localStorage.get(config['storageKeys']['token'])
    tokenAuth = localStorage.get(config['storageKeys']['tokenAuth'])

    # Not registered yet?
    if not token or not tokenAuth:
        raise Exception('This device is not registered to receive push notifications.')

    # Convert single topic to array
    if type(topics) is str:
        topics = [topics]

    # JSON post data
    postData = { 
        'token': token, 
        'auth': tokenAuth, 
        'topics': topics 
    }

    try:
        # Subscribe to topic(s)
        response = api.post('/devices/subscribe', postData)
    except Exception as err:
        # Request failed
        raise Exception('The API request failed: ' + str(err))

    # Validate response
    if not response['success']:
        raise Exception('An unexpected response was received from the Pushy API.')

def unsubscribe(topics):
    # Attempt to fetch existing token and auth
    token = localStorage.get(config['storageKeys']['token'])
    tokenAuth = localStorage.get(config['storageKeys']['tokenAuth'])

    # Not registered yet?
    if not token or not tokenAuth:
        raise Exception('This device is not registered to receive push notifications.')

    # Convert single topic to array
    if type(topics) is str:
        topics = [topics]

    # JSON post data
    postData = { 
        'token': token, 
        'auth': tokenAuth, 
        'topics': topics 
    }

    try:
        # Unsubscribe from topic(s)
        response = api.post('/devices/unsubscribe', postData)
    except Exception as err:
        # Request failed
        raise Exception('The API request failed: ' + str(err))

    # Validate response
    if not response['success']:
        raise Exception('An unexpected response was received from the Pushy API.')

def setHeartbeatInterval(seconds):
    # Invalid keepalive value?
    if not seconds or not int(seconds) or seconds < 5:
        raise Exception('Please provide a valid heartbeat interval in seconds.')

    # Save keep alive interval
    localStorage.set(config['storageKeys']['keepAliveInterval'], str(seconds))

def isEnterpriseConfigured():
    # Check whether the key is set
    return localStorage.get(config['storageKeys']['enterpriseEndpoint']) != None

def setEnterpriseConfig(endpoint, mqttEndpoint):
    # Clear requested?
    if not endpoint or not mqttEndpoint:
        # Clear saved credentials and config
        localStorage.delete(config['storageKeys']['token'])
        localStorage.delete(config['storageKeys']['tokenAuth'])
        localStorage.delete(config['storageKeys']['tokenAppId'])
        localStorage.delete(config['storageKeys']['enterpriseEndpoint'])
        localStorage.delete(config['storageKeys']['enterpriseMqttEndpoint'])

        # Disconnect any existing connection and stop execution
        return mqtt.disconnect()

    # Strip trailing slash from API endpoint
    if endpoint[-1] == '/':
        endpoint = endpoint[0, endpoint.length - 1]

    # Strip trailing slash from mqtt endpoint
    if mqttEndpoint[-1] == '/':
        mqttEndpoint = mqttEndpoint[0, mqttEndpoint.length - 1]

    # Strip ssl:// protocol prefix from mqtt endpoint
    mqttEndpoint = mqttEndpoint.replace('ssl://', '')

    # Retrieve previous endpoint (may be null)
    previousEndpoint = localStorage.get(config['storageKeys']['enterpriseEndpoint'])
    previousMqttEndpoint = localStorage.get(config['storageKeys']['enterpriseMqttEndpoint'])

    # Endpoint changed?
    if endpoint != previousEndpoint or mqttEndpoint != previousMqttEndpoint:
        # Clear existing registration
        localStorage.delete(config['storageKeys']['token'])
        localStorage.delete(config['storageKeys']['tokenAuth'])
        localStorage.delete(config['storageKeys']['tokenAppId'])

        # Save updated Pushy Enterprise hostnames in local storage
        localStorage.set(config['storageKeys']['enterpriseEndpoint'], endpoint)
        localStorage.set(config['storageKeys']['enterpriseMqttEndpoint'], mqttEndpoint)

def disconnect():
    # Attempt to disconnect from Pushy
    mqtt.disconnect()