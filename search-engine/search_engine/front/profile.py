import re

from flask import flash, render_template, redirect, request, session, url_for

from search_engine.front import app, links, texts
from search_engine.front.auth import login_required


@app.route('/')
@login_required
def index():
    user_links = links.get_by_user(session['username'])
    return render_template('index.html', user_links=user_links)


@app.route('/search')
@login_required
def search():
    query = request.args.get('query')
    if not query:
        flash('Поисковый запрос не введён', 'error')
        return redirect(url_for('index'))

    hits = texts.search(session['username'], query)
    for item in hits['hits']:
        highlighted = ' … '.join(item['highlight']['text'])
        item['highlighted'] = re.sub(r'<(/?)em>', r'<\1strong>', highlighted)
    return render_template('search.html', query=query, hits=hits)


@app.route('/crawl', methods=['POST'])
@login_required
def crawl_submit():
    url = request.form.get('url')
    if not url:
        flash('URL не введён', 'error')
        return redirect(url_for('index'))
    if not (url.startswith('http://') or url.startswith('https://')):
        flash('URL должен начинаться с "http://" или "https://"', 'error')
        return redirect(url_for('index'))
    if '.local' in url:
        flash('Запрещено индексировать ресурсы внутренней сети')
        return redirect(url_for('index'))
    username = session['username']

    links.delete_by_user(username)
    texts.delete_by_user(username)

    links.save(username, [url], 0, force_status=True)
    return redirect(url_for('index'))
