#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A fake db connector just for testing"""

from marucat_app.runtime_errors import NoSuchArticle


class ArticlesConnector(object):
    """A fake API for testing"""
    @staticmethod
    def get_list(*, size, page):
        """get a list of articles

        :param size: length of list
        :param page: start position of list
        """
        return [{'id': 1, 'size': size}, {'id': 2, 'page': page}]

    @staticmethod
    def get_content(article_id):
        """get article content

        :param article_id: identity of article
        """
        return {'id': article_id, 'content': 'The content of article.'}

    @staticmethod
    def update_views(article_id):
        """update views every times the article was visited

        :param article_id: identity of article
        """
        if article_id == 'TEST_NOT_FOUND':
            raise NoSuchArticle('No such article.')
        return {'views': 12345, 'views_id': article_id}
