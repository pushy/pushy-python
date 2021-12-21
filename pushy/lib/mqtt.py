import json
import time
import ssl
import pushy
from pushy.util.config import config
import paho.mqtt.client as mqtt
import pushy.util.localStorage as localStorage

# Default client
client = mqtt.Client()

def getMqttEndpoint():
    # Attempt to fetch Pushy Enterprise hostname (fall back to Pushy Pro endpoint)
    endpoint = localStorage.get(config['storageKeys']['enterpriseMqttEndpoint']) or config['mqtt']['endpoint']

    # Get current unix timestamp (for timestamp injection)
    unix = str(int(time.time()))

    # Inject unix timestamp into hostname (if placeholder present)
    return endpoint.replace('{timestamp}', unix)

def getMqttPort():
    # Attempt to fetch Pushy Enterprise hostname to check if running in enterprise mode
    if localStorage.get(config['storageKeys']['enterpriseMqttEndpoint']):
        # Pushy Enterprise port number
        port = config['mqtt']['enterprisePortNumber']
    else:
        # Pushy Pro port number
        port = config['mqtt']['portNumber']

    # Return port number as an integer
    return int(port)

def getMqttKeepAlive():
    # Fetch custom keepalive interval (in seconds) or default to 300
    keepAliveInterval = localStorage.get(config['storageKeys']['keepAliveInterval']) or config['mqtt']['defaultKeepAlive']

    # Convert to integer
    return int(keepAliveInterval)

def setNotificationListener(listener):
    # Set global variable
    global notificationListener

    # Store reference to listener callback method
    notificationListener = listener

def setConnectionListener(listener):
    # Set global variable
    global connectionListener

    # Store reference to listener callback method
    connectionListener = listener

def setDisconnectionListener(listener):
    # Set global variable
    global disconnectionListener

    # Store reference to listener callback method
    disconnectionListener = listener

# Callback for when the MQTT client connects successfully
def on_connect(client, userdata, flags, rc):
    # Log connection success to console
    print('[Pushy] Connected successfully (device token ' + localStorage.get(config['storageKeys']['token']) + ')')

    # Check if connection listener defined & invoke it
    if connectionListener:
        connectionListener()

# Callback for when the MQTT client disconnects
def on_disconnect(client, userdata, msg):
    # Log disconnection to console
    print('[Pushy] Disconnected from server')
    
    # Check if disconnection listener defined & invoke it
    if disconnectionListener:
        disconnectionListener()

# Callback for when the MQTT client receives a notification
def on_message(client, userdata, msg):
    # Check if notification listener defined, otherwise do nothing
    if notificationListener:
        # Decode payload into UTF-8 string
        message = msg.payload.decode('utf-8')

        try:
            # Attempt to parse message into JSON
            payload = json.loads(message)

            # Invoke notification listener with JSON dictionary
            notificationListener(payload)
        except Exception as err:
            # Log error to console
            print('[Pushy] MQTT JSON Parse Error\n' + str(err))

def connect():
    # Device not registered yet?
    if not pushy.isRegistered():
        return

    # If client socket exists, don't recreate it
    # A disconnected client will reconnect automatically
    if client._sock:
        return
    
    # Attempt to fetch existing token and auth
    token = localStorage.get(config['storageKeys']['token'])
    tokenAuth = localStorage.get(config['storageKeys']['tokenAuth'])

    # Reinitialize client with Pushy device token
    client.reinitialise(client_id=token)

    # Reset event listeners after reinitializing
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    # Set username and password accordingly
    client.username_pw_set(token, password=tokenAuth)

    # Enforce TLS encryption
    client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None)
    
    try:
        # Try connecting to Pushy MQTT endpoint
        client.connect(getMqttEndpoint(), getMqttPort(), getMqttKeepAlive())
    except Exception as err:
        print('[Pushy] Connection failed with error: ' + str(err))
    
def disconnect():
    # Disconnect if client socket is connected
    if client._sock:
        client.disconnect()

def loop_forever():
    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface
    if client._sock:
        client.loop_forever()