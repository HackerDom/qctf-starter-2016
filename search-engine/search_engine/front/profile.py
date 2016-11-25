from flask import flash, render_template, redirect, request, session, url_for

from search_engine.front import app, links, texts
from search_engine.front.auth import login_required


@app.route('/')
@login_required
def index():
    user_links = links.get_by_user(session['login'])
    return render_template('index.html', user_links=user_links)


@app.route('/search')
@login_required
def search():
    query = request.args.get('query')
    if not query:
        flash('Поисковый запрос не введён', 'error')
        return redirect(url_for('index'))

    results = texts.search(query)
    return render_template('search.html', results=results)


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

    links.save(session['url'], [url], 0, force_status=True)
    return redirect(url_for('index'))
