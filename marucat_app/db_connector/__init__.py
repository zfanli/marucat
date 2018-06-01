#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""DB connector API define here"""

from logging import getLogger
from marucat_app.db_connector.fake_articles_connector import ArticlesConnector

logger = getLogger()


class Articles(object):
    """All API about articles"""
    def __init__(self, articles_connector, logger):
        self._connector = articles_connector
        self._logger = logger

    def get_list(self):
        result = self._connector.get_list()
        self._logger.info('articles/get_list is executed')
        return result


class ConnectorCreator(object):
    """Create connector"""
    def __init__(self):
        self._articles = Articles(ArticlesConnector(), logger)

    @property
    def articles_connector(self):
        return self._articles
