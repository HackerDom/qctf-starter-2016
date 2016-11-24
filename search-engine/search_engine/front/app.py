import logging
import os
import requests
from elasticsearch import Elasticsearch
from flask import Flask, flash, redirect, request, session, url_for
from pymongo import MongoClient

from search_engine import db, settings


logging.basicConfig(format='%(levelname)s\t%(asctime)s\t%(name)s\t%(message)s', datefmt='%H:%M:%S')


app = Flask(__name__)
app.secret_key = os.environ('FLASK_SECRET_KEY')

mongo = MongoClient(settings.MONGO_URI)[settings.MONGO_DB_NAME]
es = Elasticsearch(timeout=30)

links = db.LinkDAO(mongo)
texts = db.TextDAO(es)


@app.route('/')
def index():
    pass


@app.route('/login')
def login():
    if not request.form.get('login'):
        flash('No login provided')
        return redirect(url_for(index))
    if not request.form.get('password'):
        flash('No password provided')
        return redirect(url_for(index))

    response = requests.get(settings.AUTH_SERVICE_URL + 'login/' + request)
    if not response.ok:
        flash('Auth service is unavailable')
        return redirect(url_for(index))

    user = response.json()
    if 'error' in user or request.form['password'] != user['password']:
        flash('Invalid login or password')
        return redirect(url_for(index))

    session['login'] = login
    logging.info('User "%s" logged in', login)

    return redirect(url_for(index))


@app.route('/logout')
def logout():
    if 'login' in session:
        logging.info('User "%s" logged out', session['login'])
        del session['login']

    return redirect(url_for(index))
