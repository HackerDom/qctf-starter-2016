from flask import Flask
import memcache
import sqlite3

from controllers import Controllers
from services import UserService, PhotoService
from cache import PhotoCache
from geoip import GeoIpResolver
from constants import DB_PATH, MEMCACHED_PARAMS, IP_TO_CITY_PATH, CITY_TO_COORDS_PATH, SERVER_PORT, SERVER_DEBUG


def main():
    db_connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    user_service = UserService(db_connection)
    photo_service = PhotoService(db_connection)
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
    app.add_url_rule('/upload', view_func=controllers.upload, methods=['GET', 'POST'])

    app.run(port=SERVER_PORT, debug=SERVER_DEBUG)


if __name__ == '__main__':
    main()
