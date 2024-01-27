import configparser

# Initialize the ConfigParser
config = configparser.ConfigParser()

# Read the ini file
config.read('cfg.ini')

# API Configuration
API_KEY = config.get('API', 'API_KEY')
API_URL = config.get('API', 'API_URL')

# Network Configuration
HOST = config.get('Network', 'HOST')
PORT = config.getint('Network', 'PORT')  # Use getint for integers

# Payment Configuration
AMOUNT_THRESHOLD = config.getfloat('Payment', 'AMOUNT_THRESHOLD')  # Use getfloat for floating-point numbers
POST_PAYMENT_DELAY = config.getint('Payment', 'POST_PAYMENT_DELAY')
CHECK_INTERVAL = config.getint('Payment', 'CHECK_INTERVAL')

# Camera Configuration
TRIGGER_PHOTO_COMMAND = config.get('Camera', 'TRIGGER_PHOTO_COMMAND')
DOWNLOAD_PHOTOS_COMMAND = config.get('Camera', 'DOWNLOAD_PHOTOS_COMMAND')
CLEAR_FILES_COMMAND = config.get('Camera', 'CLEAR_FILES_COMMAND')

# Storage Configuration
PICTURE_SAVE_DIRECTORY = config.get('Storage', 'PICTURE_SAVE_DIRECTORY')
FOLDER_NAME_FORMAT = config.get('Storage', 'FOLDER_NAME_FORMAT')
PICTURE_NAME_FORMAT = config.get('Storage', 'PICTURE_NAME_FORMAT')

# System Configuration
PROCESS_TO_KILL = config.get('System', 'PROCESS_TO_KILL')

# Display Configuration
FULLSCREEN_MODE = config.getboolean('Display', 'FULLSCREEN_MODE')  # Use getboolean for True/False
WINDOW_TITLE = config.get('Display', 'WINDOW_TITLE')
IMAGE_PATH = config.get('Display', 'IMAGE_PATH')
IMAGE_WIDTH = config.getint('Display', 'IMAGE_WIDTH')
IMAGE_HEIGHT = config.getint('Display', 'IMAGE_HEIGHT')
DEFAULT_TEXT = config.get('Display', 'DEFAULT_TEXT')

# Server Configuration
SERVER_HOST = config.get('Server', 'SERVER_HOST')
SERVER_PORT = config.getint('Server', 'SERVER_PORT')
MAX_CONNECTIONS = config.getint('Server', 'MAX_CONNECTIONS')
