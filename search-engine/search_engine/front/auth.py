import logging
import re
from functools import wraps

import requests
from flask import flash, redirect, render_template, request, session, url_for

from search_engine import settings
from search_engine.front import app


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_submit():
    if not request.form.get('login'):
        flash('Логин не введён', 'error')
        return redirect(url_for('index'))
    if not request.form.get('password'):
        flash('Пароль не введён', 'error')
        return redirect(url_for('index'))

    response = requests.get('http://auth.local/login/' + request)
    if not response.ok:
        flash('Сервис аутентификации недоступен', 'error')
        return redirect(url_for('index'))

    user = response.json()
    if 'error' in user or request.form['password'] != user['password']:
        flash('Неправильный логин или пароль', 'error')
        return redirect(url_for('index'))
    login = user['_id']

    session['login'] = login
    logging.info('User "%s" logged in', login)

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    if 'login' in session:
        logging.info('User "%s" logged out', session['login'])
        del session['login']

    return redirect(url_for('index'))


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_submit():
    login = request.form.get('login')
    try:
        check_login(login)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('index'))
    password = request.form.get('password')
    if not password:
        flash('Пароль не введён', 'error')
        return redirect(url_for('index'))

    response = requests.post('http://auth.local/register', json={'_id': login, 'password': password})
    if not response.ok:
        flash('Сервис аутентификации недоступен', 'error')
        return redirect(url_for('index'))

    registered = response.json()
    if not registered:
        flash('Пользователь с таким логином уже существует', 'error')
        return redirect(url_for('index'))

    session['login'] = login
    logging.info('User "%s" registered and logged in', login)

    return redirect(url_for('index'))


def check_login(login):
    if not login:
        raise ValueError('Логин не введён')
    if not (3 <= len(login) <= 10):
        raise ValueError('Логин должен содержать от 3 до 10 символов')
    if re.fullmatch(r'\w+', login) is None:
        raise ValueError('Логин может содержать только английские буквы, цифры и подчёркивания')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function
