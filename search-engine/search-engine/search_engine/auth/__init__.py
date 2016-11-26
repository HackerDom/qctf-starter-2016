from flask import Flask, jsonify, request
from pymongo import MongoClient

from search_engine import db, settings


app = Flask(__name__)

mongo = MongoClient(settings.MONGO_URI)[settings.MONGO_DB_NAME]
users = db.UserDAO(mongo)


@app.route('/login/<username>')
def login(username: str):
    user = users.find(username)
    if user is None:
        return jsonify({'error': 'User not found'})

    return jsonify(user)


@app.route('/register', methods=['POST'])
def register():
    return jsonify(users.register(request.get_json()))
