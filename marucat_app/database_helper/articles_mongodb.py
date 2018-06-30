#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Articles connector, driven by MongoDB."""

# from marucat_app.utils.errors import NoSuchArticleError, NoSuchCommentError
from marucat_app.utils.utils import deal_with_object_id
from bson import ObjectId


class ArticlesConnector(object):
    """Articles connector

    Driven by MongoDB.
    """
    def __init__(self, collection):
        """Initial mongodb connector

        :param collection: database instance
        """
        self._collection = collection

    def get_list(self, *, size, offset, tags=None):
        """Fetch articles' list

        When size is equals to zero, it is mean fetch all of the articles.

        :param size: length of list
        :param offset: counts of skips
        :param tags: tags
        """

        # edit condition
        condition = {'deleted': False}
        if tags:
            condition['tags'] = tags

        # fetch format
        projection = {
            '_id': 1,
            'author': 1,
            'peek': 1,
            'views': 1,
            'comments': 1,
            'tags': 1,
            'timestamp': 1
        }

        # fetch list
        cur = self._collection.find(condition, projection).skip(offset).limit(size)

        # check if nothing was fetched
        if cur.count() == 0:
            return None

        # convert to list
        result = [i for i in cur]
        # set counts of comments and remove the array
        for i in result:
            i['reviews'] = len(i['comments'])
            del i['comments']
        # convert ObjectId to str and return
        return deal_with_object_id(result)

    def get_content(self, article_id, *, comments_size):
        """Fetch article content

        Every times fetch the content of article,
        update the counts of views.

        :param article_id: article ID
        :param comments_size: fetch comments size
        :raise: 404 NoSuchArticleError
        """
        # TODO

        condition = {'_id': ObjectId(article_id)}

        data = self._collection.find_one(condition)

        return deal_with_object_id(data)

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

    def get_articles_count(self):
        """Get articles count

        :return: counts of articles
        """
        return self._collection.find({'deleted': False}).count()
