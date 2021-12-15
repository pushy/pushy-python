import pushy

# Initialize SDK
pushy.listen()

try:
    # Register device for push notifications
    deviceToken = pushy.register({ 'appId': '550ee57c5b5d72117f51e801' })
    
    # Persist the device token in your backend database
except Exception as err:
    # Print error to console
    print('Pushy registration error: ' + str(err))

# Define a method to process incoming notifications
def backgroundNotificationListener(data):
    # Print notification payload to console
    print('Received notification: ' + str(data))

    # Execute any custom logic here

# Set up the notification listener
pushy.setNotificationListener(backgroundNotificationListener)

# Avoid program termination (keeps your Python app from terminating until you call pushy.disconnect())
pushy.loop_forever()

# Send yourself a test notification from the demo page
# https://pushy.me/docs/resources/demo