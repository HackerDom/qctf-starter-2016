from flask import Flask
import memcache
import sqlite3

from controllers import Controllers
from services import UsersService, PhotosService
from cache import PhotoCache
from geoip import GeoIPResolver


def main():
    db_connection = sqlite3.connect('db.sqlite', check_same_thread=False)
    users_service = UsersService(db_connection)
    photos_service = PhotosService(db_connection)
    memcache_client = memcache.Client(['127.0.0.1', '11211'], debug=True, check_keys=False)
    photos_cache = PhotoCache(memcache_client, photos_service)
    geoip_resolver = GeoIPResolver('ips.txt', 'cities.txt')

    app = Flask(__name__)
    controllers = Controllers(app, users_service, photos_service, photos_cache, geoip_resolver)

    app.add_url_rule('/logout', view_func=controllers.logout)
    app.add_url_rule('/login', view_func=controllers.login, methods=['GET', 'POST'])
    app.add_url_rule('/register', view_func=controllers.register, methods=['GET', 'POST'])
    app.add_url_rule('/', view_func=controllers.root)
    app.add_url_rule('/my', view_func=controllers.my)
    app.add_url_rule('/nearby', view_func=controllers.nearby)
    app.add_url_rule('/featured', view_func=controllers.featured)
    app.add_url_rule('/upload', view_func=controllers.upload, methods=['GET', 'POST'])

    app.run(port=4567, debug=True)


if __name__ == '__main__':
    main()
