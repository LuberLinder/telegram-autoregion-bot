import configparser

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config.get('Credentials', 'TOKEN')
APP_URL = config.get('Credentials', 'APP_URL')
API_URL = config.get('Settings', 'API_URL')
BOT_URL = config.get('Settings', 'BOT_URL') + TOKEN + '/'
DEFAULT = {
    'country_id': 1,
    'lang_id': 3,
}