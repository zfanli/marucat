#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""DB connector API defined here"""

from functools import wraps
from logging import getLogger
from time import time

from pymongo import MongoClient

from marucat_app.database_helper.fake_articles_connector import FakeArticlesConnector
from marucat_app.database_helper.articles_mongodb import ArticlesConnector
from marucat_app.utils.errors import DatabaseNotExistError
from marucat_app.utils.utils import get_initial_file

logger = getLogger()


def log(func):
    """Decorator for logging

    Tell you the when function was called and show it's parameters.

    :param func: target function
    :return: decorator
    """
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
    """All API about articles

    Database manipulator about articles.
    """

    def __init__(self, articles_connector):
        self._connector = articles_connector

    @log
    def get_list(self, *, size, offset, tags):
        """fetch articles list

        :param size: fetch size
        :param offset: counts of skips
        :param tags: tags
        """
        return self._connector.get_list(size=size, offset=offset, tags=tags)

    @log
    def get_content(self, article_id, *, comments_size):
        """fetch article content

        :param article_id: article ID
        :param comments_size: fetch comments size
        """
        return self._connector.get_content(article_id, comments_size=comments_size)

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
        :return: list of comments
        """
        return self._connector.get_comments(article_id, size=size, page=page)

    @log
    def post_comment(self, article_id, *, data):
        """Post new comment

        Post data should be checked before this method.

        :param article_id: article ID
        :param data: json data
        """
        self._connector.post_comment(article_id, data=data)

    @log
    def delete_comment(self, article_id, comment_id):
        """Delete a comment

        :param article_id: article ID
        :param comment_id: comment ID
        """
        self._connector.delete_comment(article_id, comment_id)


class ConnectorCreator(object):
    """Create connector

    Use to instance a database helper.
    """

    def __init__(self, db):
        """Initial database connection

        :param db: specified database
        """
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

        # get ini file
        conf = get_initial_file()
        # get necessary information from ini file
        mongo_conf = conf['mongodb']
        url = mongo_conf['url']
        port = int(mongo_conf['port'])
        schema = mongo_conf['schema']
        articles_collection = mongo_conf['articles_collection']
        # initial mongodb connection
        client = MongoClient(url, port)

        # test connection
        # leave a log show the connect time
        db = client[schema]
        connect_log = db.connect_log
        connect_log.insert_one({'time': time()})

        # initial mongodb connector
        # Articles: SCHEMA/articles
        self._articles = Articles(ArticlesConnector(db[articles_collection]))

    @property
    def articles_helper(self):
        return self._articles


if __name__ == '__main__':
    c = ConnectorCreator('test')
    getattr(c, 'articles_connector')
