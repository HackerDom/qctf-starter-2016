import logging
import re
from functools import wraps
from urllib.parse import urljoin

import requests
from flask import flash, redirect, render_template, request, session, url_for

from search_engine import settings
from search_engine.front import app


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form.get('username')
    if not username:
        flash('Имя пользователя не введено', 'error')
        return redirect(url_for('index'))
    if not request.form.get('password'):
        flash('Пароль не введён', 'error')
        return redirect(url_for('index'))

    response = requests.get(urljoin(settings.AUTH_SERVICE_URI, '/login/' + username))
    if not response.ok:
        flash('Сервис аутентификации недоступен', 'error')
        return redirect(url_for('index'))

    user = response.json()
    if 'error' in user or request.form['password'] != user['password']:
        flash('Неправильный логин или пароль', 'error')
        return redirect(url_for('index'))

    session['username'] = username
    logging.info('User "%s" logged in', username)

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    if 'username' in session:
        logging.info('User "%s" logged out', session['username'])
        del session['username']

    return redirect(url_for('index'))


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_submit():
    username = request.form.get('username')
    try:
        check_username(username)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('index'))
    password = request.form.get('password')
    if not password:
        flash('Пароль не введён', 'error')
        return redirect(url_for('index'))

    response = requests.post(urljoin(settings.AUTH_SERVICE_URI, '/register'),
                             json={'_id': username, 'password': password})
    if not response.ok:
        flash('Сервис аутентификации недоступен', 'error')
        return redirect(url_for('index'))

    registered = response.json()
    if not registered:
        flash('Пользователь с таким логином уже существует', 'error')
        return redirect(url_for('index'))

    session['username'] = username
    logging.info('User "%s" registered and logged in', username)

    return redirect(url_for('index'))


def check_username(username):
    if not username:
        raise ValueError('Логин не введён')
    if not (3 <= len(username) <= 10):
        raise ValueError('Логин должен содержать от 3 до 10 символов')
    if re.fullmatch(r'\w+', username) is None:
        raise ValueError('Логин может содержать только английские буквы, цифры и подчёркивания')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function
