import os
import configparser

# Read config.ini file in parent directory
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../', 'config.ini'))