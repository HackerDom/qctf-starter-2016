import logging
import time
import traceback

import requests
from pyquery import PyQuery

from search_engine import db


class Crawler:
    def __init__(self, name: str, links: db.LinkDAO, texts: db.TextDAO):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

        self._links = links
        self._texts = texts

    def run(self):
        while True:
            found = self._check_next()

            if not found:
                self._logger.debug('No links in the queue, sleeping')
                time.sleep(Crawler._NOT_FOUND_DELAY)

    _NOT_FOUND_DELAY = 3

    def _check_next(self) -> bool:
        processed_link = self._links.select_next()
        if processed_link is None:
            return False
        username = processed_link['username']
        url = processed_link['url']

        try:
            response = requests.get(url, timeout=Crawler._REQUEST_TIMEOUT)
            if response.status_code != 200:
                self._links.update_status(username, url, 'failed', reason=response.status_code)
                return True

            content = response.content
            if len(content) > Crawler._MAX_PAGE_SIZE:
                raise ValueError('Too big page ({} bytes)'.format(len(content)))

            d = PyQuery(content)
            d.remove('script, style')
            title = d('title').text()
            body = d('body')
            text = (body if body else d).text()

            self._texts.save(username, url, title, text)

            message = '@{}: {} crawled'.format(username, url)

            if processed_link['distance'] < Crawler._MAX_DEPTH:
                links = [url for url in d('a[href]').map(lambda _, el: d(el).attr('href'))
                         if url.startswith('http://') or url.startswith('https://')]
                links = links[:Crawler._MAX_LINKS]

                self._links.save(username, links, processed_link['distance'] + 1, force_status=False)

                message += ', {} links added'.format(len(links))

            self._links.update_status(username, url, 'crawled')
            self._logger.info(message)
        except Exception as e:
            self._links.update_status(username, url, 'failed', reason='{}: {}'.format(type(e).__name__, e))

            self._logger.warning('Exception on requesting page: %s', e)
            traceback.print_exc()
        return True

    _MAX_DEPTH = 2

    _MAX_PAGE_SIZE = 1024 * 1024
    _MAX_LINKS = 20

    _REQUEST_TIMEOUT = 3
