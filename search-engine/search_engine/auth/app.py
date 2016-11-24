from flask import Flask, jsonify, request
from pymongo import MongoClient

from search_engine import db, settings


app = Flask(__name__)

mongo = MongoClient(settings.MONGO_URI)[settings.MONGO_DB_NAME]
users = db.UserDAO(mongo)


@app.route('/info/<login>', methods=['GET'])
def get_info(login: str):
    user = users.find(login)
    if user is None:
        return jsonify({'error': 'User not found'})

    return jsonify(user)


@app.route('/register', methods=['POST'])
def set_info():
    return jsonify(users.register(request.get_json()))
