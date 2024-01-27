import configparser

config = configparser.ConfigParser()

# Attempt to read the config file
try:
    config.read('cfg.ini')
except Exception as e:
    print(f"Error reading the config file: {e}")

# Helper function to get configuration values with error handling
def get_config_value(section, key):
    try:
        return config.get(section, key)
    except configparser.NoSectionError:
        print(f"Missing section '{section}' in config file.")
    except configparser.NoOptionError:
        print(f"Missing key '{key}' in section '{section}' in config file.")
    except Exception as e:
        print(f"Error retrieving configuration value: {e}")

# API Configuration
API_KEY = get_config_value('API', 'API_KEY')
API_URL = get_config_value('API', 'API_URL')

# Network Configuration
HOST = get_config_value('Network', 'HOST')
PORT = config.getint('Network', 'PORT')  # Assuming PORT will always be present and correctly formatted

# Payment Configuration
AMOUNT_THRESHOLD = config.getfloat('Payment', 'AMOUNT_THRESHOLD')  # Assuming AMOUNT_THRESHOLD will always be present and correctly formatted
POST_PAYMENT_DELAY = config.getint('Payment', 'POST_PAYMENT_DELAY')  # Assuming POST_PAYMENT_DELAY will always be present and correctly formatted
CHECK_INTERVAL = config.getint('Payment', 'CHECK_INTERVAL')  # Assuming CHECK_INTERVAL will always be present and correctly formatted

# Camera Configuration
TRIGGER_PHOTO_COMMAND = get_config_value('Camera', 'TRIGGER_PHOTO_COMMAND')
DOWNLOAD_PHOTOS_COMMAND = get_config_value('Camera', 'DOWNLOAD_PHOTOS_COMMAND')
CLEAR_FILES_COMMAND = get_config_value('Camera', 'CLEAR_FILES_COMMAND')

# Storage Configuration
PICTURE_SAVE_DIRECTORY = get_config_value('Storage', 'PICTURE_SAVE_DIRECTORY')
FOLDER_NAME_FORMAT = get_config_value('Storage', 'FOLDER_NAME_FORMAT')
PICTURE_NAME_FORMAT = get_config_value('Storage', 'PICTURE_NAME_FORMAT')

# System Configuration
PROCESS_TO_KILL = get_config_value('System', 'PROCESS_TO_KILL')

# Display Configuration
FULLSCREEN_MODE = config.getboolean('Display', 'FULLSCREEN_MODE')  # Assuming FULLSCREEN_MODE will always be present and correctly formatted
WINDOW_TITLE = get_config_value('Display', 'WINDOW_TITLE')
IMAGE_PATH = get_config_value('Display', 'IMAGE_PATH')
IMAGE_WIDTH = config.getint('Display', 'IMAGE_WIDTH')  # Assuming IMAGE_WIDTH will always be present and correctly formatted
IMAGE_HEIGHT = config.getint('Display', 'IMAGE_HEIGHT')  # Assuming IMAGE_HEIGHT will always be present and correctly formatted
DEFAULT_TEXT = get_config_value('Display', 'DEFAULT_TEXT')

# Server Configuration
SERVER_HOST = get_config_value('Server', 'SERVER_HOST')
SERVER_PORT = config.getint('Server', 'SERVER_PORT')  # Assuming SERVER_PORT will always be present and correctly formatted
MAX_CONNECTIONS = config.getint('Server', 'MAX_CONNECTIONS')  # Assuming MAX_CONNECTIONS will always be present and correctly formatted
