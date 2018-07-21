#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""DB connector API defined here"""

from functools import wraps
from logging import getLogger

from pymongo import MongoClient

from marucat_app.database_helper.fake_articles_connector import FakeArticlesConnector
from marucat_app.database_helper.articles_mongodb import ArticlesConnector
from marucat_app.database_helper.settings_mogodb import SettingsConnector
from marucat_app.utils.errors import DatabaseNotExistError
from marucat_app.utils.utils import get_initial_file, get_current_time_in_milliseconds

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
    def get_comments(self, article_id, *, size, offset):
        """fetch comments of specific article

        :param article_id: article ID
        :param size: fetch size
        :param offset: fetch start position
        :return: list of comments, count
        """
        return self._connector.get_comments(article_id, size=size, offset=offset)

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

    @log
    def get_articles_counts(self):
        """Get articles counts

        :return: int, counts of articles
        """
        return self._connector.get_articles_counts()


class Settings(object):
    """For manipulate settings"""

    def __init__(self, settings_connector):
        self._connector = settings_connector

    def get_list(self, *, size, offset):
        """Get settings list

        :param size: paging size
        :param offset: skip
        :return: list of settings
        """
        return self._connector.get_list(size=size, offset=offset)

    def get_one(self, name):
        """Get specified one of settings

        :param name: name
        :return: specified one
        """
        return self._connector.get_one(name)

    def update_one(self, name, data):
        """Update settings

        :param name: name
        :param data: data
        :return: updated object
        """
        return self._connector.update_one(name, data)

    def delete_one(self, name):
        """Delete specified one of settings

        :param name: name
        :return: True or False tell you
        """
        return self._connector.delete_one(name)


class ConnectorCreator(object):
    """Create connector

    Use to instance a database helper.
    """

    def __init__(self, db, *, test=False):
        """Initial database connection

        :param db: specified database
        """
        if db == 'test':
            # TEST mode load fake db helper
            self._articles = Articles(FakeArticlesConnector())
            self._settings = None
        elif db == 'mongodb':
            # load MongoDB helper
            self.init_mongodb(test)
        else:
            # Specific db is not supported
            raise DatabaseNotExistError(
                'Specific Database do not exist: {}'.format(db)
            )

    def init_mongodb(self, test_flag):
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
        logs_collection = mongo_conf['logs_collection']

        # if test flag is True set current schema to test schema
        if test_flag:
            schema = mongo_conf['test_schema']

        articles_collection = mongo_conf['articles_collection']
        settings_collection = mongo_conf['settings_collection']
        # initial mongodb connection
        client = MongoClient(url, port)

        # test connection
        # leave a log show the connect time
        db = client[schema]
        connect_log = db[logs_collection]
        connect_log.insert_one({'time': get_current_time_in_milliseconds()})

        # initial mongodb connector
        # Articles: SCHEMA/articles
        self._articles = Articles(ArticlesConnector(db[articles_collection]))
        # Settings: SCHEMA/settings
        self._settings = Settings(SettingsConnector(db[settings_collection]))

    @property
    def articles_helper(self):
        """Get articles helper

        :return: articles helper
        """
        return self._articles

    @property
    def settings_helper(self):
        """Get settings helper

        :return: settings helper
        """
        return self._settings


if __name__ == '__main__':
    c = ConnectorCreator('mongodb')
    assert getattr(c, 'articles_helper')
    assert getattr(c, 'settings_helper')
