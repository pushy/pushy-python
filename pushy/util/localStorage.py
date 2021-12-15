import dbm
from pathlib import Path

# Make sure 'db' subdirectory exists
Path('db').mkdir(exist_ok=True)

# Open and/or create key value store
db = dbm.open('db/pushy', 'c')

# Getter method
def get(key):
    try:
        return db[key].decode('utf-8')
    # Return null if key doesn't exist
    except KeyError:
        return None

# Setter method
def set(key, value):
  db[key] = value

# Delete method
def delete(key):
  try:
    del db[key]
  except KeyError:
    # Do nothing if key doesn't exist
    return
