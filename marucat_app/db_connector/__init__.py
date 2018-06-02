#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""DB connector API define here"""

from logging import getLogger
from functools import wraps
from marucat_app.db_connector.fake_articles_connector import ArticlesConnector

logger = getLogger()


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        # format: Class/Method is executed. Parameter(s): (params) {kw params}
        real_args = args[1:]
        logger.info('{}/{} is executed. {}'.format(
            args[0].__class__.__name__,
            func.__name__,
            'Parameter(s): {} {}'.format(
                real_args if not real_args == () else '',
                kwargs if not kwargs == {} else ''
            ) if not kwargs == {} or not args[1:] == () else ''
        ))
        return result
    return wrapper


class Articles(object):
    """All API about articles"""
    def __init__(self, articles_connector):
        self._connector = articles_connector

    @log
    def get_list(self, *, size, page):
        return self._connector.get_list(size=size, page=page)

    @log
    def get_content(self):
        pass


class ConnectorCreator(object):
    """Create connector"""
    def __init__(self):
        self._articles = Articles(ArticlesConnector())

    @property
    def articles_connector(self):
        return self._articles


if __name__ == '__main__':
    o = ConnectorCreator()
    a = o.articles_connector
    a.get_list(size=10, page=1)
