import os


AUTH_SERVICE_URI = 'http://auth.local'

MONGO_URI = 'mongodb://mongo:27017/'
MONGO_DB_NAME = 'search_engine'

ES_HOSTS = ['elasticsearch:9200']
ES_INDEX_NAME = 'search_engine'

CRAWLER_THREADS = 40

SECRET_KEY = os.environ['FLASK_SECRET_KEY']
