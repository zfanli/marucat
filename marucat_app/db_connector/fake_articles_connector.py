#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A fake db connector just for testing"""

from marucat_app.errors import NoSuchArticleError


class FakeArticlesConnector(object):
    """A fake API for testing"""

    @staticmethod
    def get_list(*, size, page):
        """get a list of articles

        :param size: length of list
        :param page: start position of list
        """

        fake_data = [
            {
                'aid': 'ID_OF_ARTICLE',
                'author': 'THE AUTHOR',
                'peek': 'A peek of the content of requested article.',
                'views': 998,
                'likes': 13,
                'reviews': 8,
                'timestamp': 1528969644.344048
            },
            {
                'test_only': 'TESTING',
                'size': size,
                'page': page
            }
        ]

        return fake_data

    @staticmethod
    def get_content(article_id):
        """get article content

        :param article_id: identity of article
        """
        if article_id == 'TEST_NOT_FOUND':
            raise NoSuchArticleError('No such article.')
        return {'id': article_id, 'content': 'The content of article.'}

    @staticmethod
    def update_views(article_id):
        """update views every times the article was visited

        :param article_id: identity of article
        """
        return {'views': 12345, 'views_id': article_id}

    @staticmethod
    def get_comments(article_id, *, size, page):
        """get article content

        :param article_id: identity of article
        :param size: fetch size
        :param page: fetch start position
        """
        if article_id == 'TEST_NOT_FOUND':
            raise NoSuchArticleError('No such article.')
        return {
            'id': article_id,
            'comments': 'Test comments',
            'size': size,
            'page': page
        }
