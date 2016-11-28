from flask import Flask, g
import memcache
import MySQLdb

from controllers import Controllers
from services import UserService, PhotoService
from cache import PhotoCache
from geoip import GeoIpResolver
from constants import *


def create_db_connection():
    return MySQLdb.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER,
        password=DB_PASSWORD, database=DB_DATABASE, charset='utf8')


def request_db_connection():
    if not hasattr(g, 'db_connection'):
        g.db_connection = create_db_connection()
    return g.db_connection


def close_connection(e):
    if hasattr(g, 'db_connection'):
        g.db_connection.close()


user_service = UserService(request_db_connection)
photo_service = PhotoService(request_db_connection)
memcache_client = memcache.Client(*MEMCACHED_PARAMS)
photo_cache = PhotoCache(memcache_client, photo_service)
geoip_resolver = GeoIpResolver(IP_TO_CITY_PATH, CITY_TO_COORDS_PATH)
controllers = Controllers(user_service, photo_service, photo_cache, geoip_resolver)

app = Flask(__name__)
app.add_url_rule('/logout', view_func=controllers.logout)
app.add_url_rule('/login', view_func=controllers.login, methods=['GET', 'POST'])
app.add_url_rule('/register', view_func=controllers.register, methods=['GET', 'POST'])
app.add_url_rule('/', view_func=controllers.root)
app.add_url_rule('/my', view_func=controllers.my)
app.add_url_rule('/nearby', view_func=controllers.nearby)
app.add_url_rule('/featured', view_func=controllers.featured)
app.add_url_rule('/all', view_func=controllers.all)
app.add_url_rule('/upload', view_func=controllers.upload, methods=['GET', 'POST'])
app.add_url_rule('/delete', view_func=controllers.delete)

app.teardown_appcontext(close_connection)
