#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A fake db connector just for testing"""

from marucat_app.errors import NoSuchArticleError


class FakeArticlesConnector(object):
    """A fake API for testing"""

    @staticmethod
    def get_list(*, size, page):
        """Fetch articles' list

        If 'size x page' is greater than actually counts of articles,
        fetch the all rest of articles.

        :param size: length of list
        :param page: start position of list, start by 1
        """

        fake_data = [
            {
                'content': 'Fake contents'
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
        """Fetch article content

        Every times fetch the content of article,
        update the counts of views.

        :param article_id: identity of article
        """
        if article_id == 'TEST_NOT_FOUND':
            raise NoSuchArticleError('No such article.')
        return {
            'aid': article_id
        }

    @staticmethod
    def get_comments(article_id, *, size, page):
        """get article content

        :param article_id: identity of article
        :param size: fetch size
        :param page: fetch start position
        """
        if article_id == 'TEST_NOT_FOUND':
            raise NoSuchArticleError('No such article.')
        return [
            {
                'content': 'Fake contents'
            },
            {
                'test_only_aid': article_id,
                'page': page,
                'size': size
            }
        ]
