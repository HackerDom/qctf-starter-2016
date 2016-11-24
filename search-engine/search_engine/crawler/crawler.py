import logging
import time

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
        user = processed_link['user']
        url = processed_link['url']

        try:
            content = requests.get(url, timeout=Crawler._REQUEST_TIMEOUT).content
            if len(content) > Crawler._MAX_PAGE_SIZE:
                raise ValueError('Too big page ({} bytes)'.format(len(content)))

            d = PyQuery(content)

            texts = [el.strip() for el in d('body :not(script):not(style)').contents() if isinstance(el, str)]
            texts = [el for el in texts if el]
            texts = texts[:Crawler._MAX_TEXT_NODES]

            self._texts.save(user, url, texts)

            message = '@{}: {} crawled, {} text nodes indexed'.format(user, url, len(texts))

            if processed_link['distance'] < Crawler._MAX_DEPTH:
                links = [url for url in d('a[href]').map(lambda _, el: d(el).attr('href'))
                         if any(url.startswith(proto + '://') for proto in Crawler._ALLOWED_PROTOCOLS)]
                links = links[:Crawler._MAX_LINKS]

                self._links.save(user, links, processed_link['distance'] + 1, force_status=False)

                message += ', {} links added'.format(len(links))

            self._links.update_status(user, url, 'crawled')
            self._logger.info(message)
        except Exception as e:
            self._links.update_status(user, url, 'failed', reason='{}: {}'.format(type(e).__name__, e))
            self._logger.warning('Exception on requesting page: %s', e)

        return True

    _MAX_DEPTH = 2

    _MAX_PAGE_SIZE = 1024 * 1024
    _MAX_TEXT_NODES = 100
    _MAX_LINKS = 20

    _REQUEST_TIMEOUT = 3

    _ALLOWED_PROTOCOLS = ['http', 'https']
