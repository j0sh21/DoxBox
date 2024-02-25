import configparser

config = configparser.ConfigParser()

try:
    config.read(r'../config/cfg.ini')
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
PORT = config.getint('Network', 'PORT')

# Payment Configuration
AMOUNT_THRESHOLD = config.getfloat('Payment', 'AMOUNT_THRESHOLD')
POST_PAYMENT_DELAY = config.getint('Payment', 'POST_PAYMENT_DELAY')
CHECK_INTERVAL = config.getint('Payment', 'CHECK_INTERVAL')

# Camera Configuration
TRIGGER_PHOTO_COMMAND = get_config_value('Camera', 'TRIGGER_PHOTO_COMMAND')
DOWNLOAD_PHOTOS_COMMAND = get_config_value('Camera', 'DOWNLOAD_PHOTOS_COMMAND')
CLEAR_FILES_COMMAND = get_config_value('Camera', 'CLEAR_FILES_COMMAND')

# Camera Error handling
IMG_SLEEP_TIME_SHORT = config.getint('ON_Error', 'IMG_SLEEP_TIME_SHORT')
IMG_SLEEP_TIME_LONG = config.getint('ON_Error', 'IMG_SLEEP_TIME_LONG')
MAX_RETRIES = config.getint('ON_Error', 'MAX_RETRIES')

# Storage Configuration
PICTURE_SAVE_DIRECTORY = get_config_value('Storage', 'PICTURE_SAVE_DIRECTORY')

# System Configuration
PROCESS_TO_KILL = get_config_value('System', 'PROCESS_TO_KILL')

# Display Configuration
FULLSCREEN_MODE = config.getboolean('Display', 'FULLSCREEN_MODE')
WINDOW_TITLE = get_config_value('Display', 'WINDOW_TITLE')
PATH_TO_FRAME= get_config_value('Display', 'PATH_TO_FRAME')
IMAGE_PATH = get_config_value('Display', 'IMAGE_PATH')

# Server Configuration
SERVER_HOST = get_config_value('Server', 'SERVER_HOST')
SERVER_PORT = config.getint('Server', 'SERVER_PORT')
MAX_CONNECTIONS = config.getint('Server', 'MAX_CONNECTIONS')

PRINTER_NAME = get_config_value('Printer', 'NAME')
PRINT_DIR = get_config_value('Printer', 'DIR')

# GPIO PINS for LED
red_pin = config.getint('GPIO', 'red_pin')
green_pin = config.getint('GPIO', 'green_pin')
blue_pin = config.getint('GPIO', 'blue_pin')

# LED effects
on_time = config.getfloat('GPIO', 'on_time')
off_time = config.getfloat('GPIO', 'off_time')
fade_steps = config.getfloat('GPIO', 'fade_steps')
brightness_steps = config.getfloat('GPIO', 'brightness_steps')
BREATH_SPEED = config.getfloat('GPIO', 'BREATH_SPEED')
BREATH_STEPS = config.getint('GPIO', 'BREATH_STEPS')

# LED Server and Client
LED_SERVER_HOST = get_config_value('LED_Server', 'SERVER_HOST')
LED_SERVER_PORT = config.getint('LED_Server', 'SERVER_PORT')

#DEBUG MODE
DEBUG_MODE = config.getint('DEV', 'DEBUG')

print("Config successfully loaded!")
