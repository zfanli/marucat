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

        When size is 0, mean fetch all of the rest articles.

        :param size: length of list
        :param offset: counts of skips
        :param tags: tags
        :return: fetched list, or None if nothing was fetched
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
            'reviews': 1,
            'tags': 1,
            'timestamp': 1
        }

        # check if size is 0 then set it to maximum (limit can not be 0)
        size = 999 if size == 0 else size

        # fetch list
        cur = self._collection.find(condition, projection).skip(offset).limit(size)

        # convert to list
        result = [i for i in cur]

        # check if nothing was fetched
        if len(result) == 0:
            return None

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

        # edit condition
        condition = {'_id': ObjectId(article_id)}

        # format
        projection = {
            '_id': 1,
            'author': 1,
            'content': 1,
            'views': 1,
            'tags': 1,
            'reviews': 1,
            'timestamp': 1
        }

        # fetch document
        data = self._collection.find_one(condition, projection)

        # fetch comments
        data['comments'] = self.get_comments(article_id, size=comments_size, offset=0)

        return deal_with_object_id(data)

    def get_comments(self, article_id, *, size, offset):
        """Get article content

        :param article_id: article ID
        :param size: fetch size
        :param offset: skip
        :raise: 404 NoSuchArticleError
        """

        # check if size is 0 then set it to maximum (limit can not be 0)
        size = 999 if size == 0 else size

        data = self._collection.aggregate([
            # unwind comment array
            {'$unwind': '$comments'},
            # match specified article and filter deleted comments
            {'$match': {'_id': ObjectId(article_id), 'comments.deleted': False}},
            # limit size
            {'$limit': size},
            # for paging
            {'$skip': offset},
            # only fetch comments
            {'$project': {'comments': {
                'aid': 1,
                'cid': 1,
                'body': 1,
                'from': 1,
                'timestamp': 1
            }}}
        ])

        # make a list and return
        return [x['comments'] for x in data]

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

    def get_articles_counts(self):
        """Get articles count

        :return: counts of articles
        """
        return self._collection.find({'deleted': False}).count()
