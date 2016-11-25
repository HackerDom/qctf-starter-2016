import os


# AUTH_SERVICE_URI = 'http://auth.local'
AUTH_SERVICE_URI = 'http://localhost:5001'

MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB_NAME = 'search_engine'

ES_HOSTS = ['localhost:9200']
ES_INDEX_NAME = 'search_engine'

CRAWLER_THREADS = 3

SECRET_KEY = os.environ['FLASK_SECRET_KEY']
