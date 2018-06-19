#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""DB connector API define here"""

from functools import wraps
from logging import getLogger

from marucat_app.database_helper.fake_articles_connector import \
    FakeArticlesConnector
from marucat_app.utils.errors import DatabaseNotExistError

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
        """fetch articles list

        :param size: fetch size
        :param page: fetch start position
        """
        return self._connector.get_list(size=size, page=page)

    @log
    def get_content(self, article_id):
        """fetch article content

        :param article_id: article ID
        """
        return self._connector.get_content(article_id)

    @log
    def update_views(self, article_id):
        """update the count of views when article was visited

        :param article_id: article ID
        """
        return self._connector.update_views(article_id)

    @log
    def get_comments(self, article_id, *, size, page):
        """fetch comments of specific article

        :param article_id: article ID
        :param size: fetch size
        :param page: fetch start position
        :return: array of comments
        """
        return self._connector.get_comments(article_id, size=size, page=page)


class ConnectorCreator(object):
    """Create connector"""
    def __init__(self, db):
        if db == 'test':
            # TEST mode load fake db helper
            self._articles = Articles(FakeArticlesConnector())
        elif db == 'mongodb':
            # load MongoDB helper
            self.init_mongodb()
        else:
            # Specific db is not supported
            raise DatabaseNotExistError(
                'Specific Database do not exist: {}'.format(db)
            )

    def init_mongodb(self):
        """Init MongoDB helper"""
        # get connection of MondoDB
        # connection = None
        # create connector use the connection of MongoDB
        # self._articles = Articles(ArticlesConnector(connection))

        # TODO just pass now
        self._articles = Articles(FakeArticlesConnector())

    @property
    def articles_connector(self):
        return self._articles


if __name__ == '__main__':
    c = ConnectorCreator('test')
    getattr(c, 'articles_connector')
