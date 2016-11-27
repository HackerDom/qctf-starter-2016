import datetime
import os
import pickle
import re


SERVER_PORT = 4567
SERVER_DEBUG = False
with open('secrets/password_secret.txt') as f:
    PASSWORD_SECRET = f.read().strip()
with open('secrets/jwt_secret.txt') as f:
    JWT_SECRET = f.read().strip()
SESSION_LENGTH = datetime.timedelta(hours=24)
MAX_PHOTO_SIZE = 20 * 1024 * 1024
MEMCACHED_HOST = 'memcached'
MEMCACHED_PORT = '11211'
MEMCACHED_PARAMS = [MEMCACHED_HOST, MEMCACHED_PORT], False, False, pickle.Pickler, pickle.Unpickler, None, None, 250, 1024 * 1024, 30, 3, False, False, False
MEMCACHED_EXPIRATION_TIME = 60
MEMCACHED_MIN_COMPRESS_LEN = 1000
DB_HOST = 'mysql'
DB_PORT = 3306
DB_USER = os.environ['MYSQL_USER']
DB_PASSWORD = os.environ['MYSQL_PASSWORD']
DB_DATABASE = os.environ['MYSQL_DATABASE']
IP_TO_CITY_PATH = 'ips.txt'
CITY_TO_COORDS_PATH = 'cities.txt'
USERNAME_RE = re.compile(r'[-\w]{4,}')
PHOTO_DIR = 'static/photos/'
