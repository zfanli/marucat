#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A fake db connector just for testing"""

from marucat_app.utils.errors import NoSuchArticleError, NoSuchCommentError


def do_something(*obj):
    """Do something with the parameters.

    :param obj:
    :return: None
    """
    print(obj)


class FakeArticlesConnector(object):
    """A fake API for testing"""

    @staticmethod
    def get_list(*, size, page, tags=None):
        """Fetch articles' list

        If 'size x page' is greater than actually counts of articles,
        fetch the all rest of articles.

        :param size: length of list
        :param page: start position of list, start by 1
        :param tags: tags
        """

        fake_data = [
            {
                'content': 'Fake contents'
            },
            {
                'test_only': 'TESTING',
                'size': size,
                'page': page,
                'tags': tags
            }
        ]

        return fake_data

    @staticmethod
    def get_content(article_id, *, comments_size):
        """Fetch article content

        Every times fetch the content of article,
        update the counts of views.

        :param article_id: article ID
        :param comments_size: fetch comments size
        """
        if article_id == 'TEST_NOT_FOUND':
            raise NoSuchArticleError('No such article.')
        return {
            'aid': article_id,
            'comments_size': comments_size
        }

    @staticmethod
    def get_comments(article_id, *, size, page):
        """get article content

        :param article_id: article ID
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

    @staticmethod
    def post_comment(article_id, *, data):
        """Post new comment

        :param article_id: article ID
        :param data: comment data
        """

        if article_id == 'TEST_NOT_FOUND':
            raise NoSuchArticleError('No such article.')

        do_something(data)

    @staticmethod
    def delete_comment(article_id, comment_id):
        """Delete a comment

        :param article_id:
        :param comment_id:
        """

        if article_id == 'TEST_NOT_FOUND':
            raise NoSuchArticleError('No such article.')
        if comment_id == 'TEST_NOT_FOUND':
            raise NoSuchCommentError('No such comment.')
