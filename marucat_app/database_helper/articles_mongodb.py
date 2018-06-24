#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Articles connector, driven by MongoDB."""

# from marucat_app.utils.errors import NoSuchArticleError, NoSuchCommentError


class ArticlesConnector(object):
    """Articles connector

    Driven by MongoDB.
    """
    def __init__(self, collection):
        """Initial mongodb connector

        :param collection: database instance
        """
        self._collection = collection

    def get_list(self, *, size, page, tags=None):
        """Fetch articles' list

        If 'size x page' is greater than actually counts of articles,
        fetch the all rest of articles.

        :param size: length of list
        :param page: start position of list, start by 1
        :param tags: tags
        """

        # edit condition
        condition = {}
        if tags:
            condition = {'tags': tags}

        # return result
        # skip previous result: size * (page - 1)
        # limit return result by size
        return self._collection.find(condition).skip(size * (page - 1)).limit(size)

    def get_content(self, article_id, *, comments_size):
        """Fetch article content

        Every times fetch the content of article,
        update the counts of views.

        :param article_id: article ID
        :param comments_size: fetch comments size
        :raise: 404 NoSuchArticleError
        """
        # TODO

    def get_comments(self, article_id, *, size, page):
        """get article content

        :param article_id: article ID
        :param size: fetch size
        :param page: fetch start position
        :raise: 404 NoSuchArticleError
        """
        # TODO

    def post_comment(self, article_id, *, data):
        """Post new comment

        :param article_id: article ID
        :param data: comment data
        :raise: 404 NoSuchArticleError
        """
        # TODO

    def delete_comment(self, article_id, comment_id):
        """Delete a comment

        :param article_id: article ID
        :param comment_id: comment ID
        :raises:
            - 404 NoSuchArticleError
            - 404 NoSuchCommentError
        """
        # TODO
