#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""DB connector API define here"""

__author__ = 'Z.Rick'

from marucat_app.db_connector.fake_articles_connector import ArticlesConnector


class Articles(object):
    """All API about articles"""
    def __init__(self, articles_connector, logger):
        self._connector = articles_connector
        self._logger = logger

    def get_lists(self):
        self._connector.get_lists()
        self._logger.info('get_lists executed')


class ConnectorCreator(object):
    """Create connector"""
    def __init__(self, logger):
        self._articles = Articles(ArticlesConnector(), logger)

    @property
    def articles_connector(self):
        return self._articles
