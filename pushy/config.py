import os
import configparser

config_string = """
[sdk]
# Pushy Python SDK version code
version = 1009
# SDK platform code
platform = python

# API endpoints (prod/dev)
[api]
endpoint = https://api.pushy.me
devEndpoint = http://localhost:3001

[mqtt]
# MQTT endpoint
endpoint = mqtt-{timestamp}.pushy.io
# MQTT port number
portNumber = 443
# Pushy Enterprise port number
enterprisePortNumber = 8883
# MQTT keep alive (in seconds)
defaultKeepAlive = 300

# Local storage preference keys
[storageKeys]
token = pushyToken
tokenAuth = pushyTokenAuth
tokenAppId = pushyTokenAppId
keepAliveInterval = pushyKeepAliveInt
enterpriseEndpoint = pushyEnterpriseEndpoint
enterpriseMqttEndpoint = pushyEnterpriseMqttEndpoint
"""

# Read config.ini file in parent directory
config = configparser.ConfigParser()
config.read_string(config_string)