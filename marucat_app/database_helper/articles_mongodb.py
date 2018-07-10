#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Articles connector, driven by MongoDB."""

from bson import ObjectId

# from marucat_app.utils.errors import NoSuchArticleError, NoSuchCommentError
from marucat_app.utils.utils import deal_with_object_id, get_current_time_in_milliseconds
from marucat_app.utils.errors import NoSuchArticleOrCommentError, NoSuchArticleError


class ArticlesConnector(object):
    """Articles connector

    Driven by MongoDB.
    """

    def __init__(self, collection):
        """Initial mongodb connector

        :param collection: database instance
        """
        self._collection = collection

    def get_list(self, *, size, offset, tags=None, fetch_deleted=False):
        """Fetch articles' list

        When size is 0, mean fetch all of the rest articles.

        :param size: length of list
        :param offset: counts of skips
        :param tags: tags
        :param fetch_deleted: fetch deleted object flag, only admin can set to True
        :return: fetched list, or None if nothing was fetched
        """

        # edit condition
        condition = {'$match': {}}
        if not fetch_deleted:
            condition['$match']['deleted'] = False
        if tags:
            condition['$match']['tags'] = tags

        # fetch format
        projection = {
            '$project': {
                '_id': 1,
                'title': 1,
                'author': 1,
                'peek': 1,
                'views': 1,
                'tags': 1,
                'timestamp': 1,
                'deleted': 1,
                'reviews': {
                    '$size': {
                        '$filter': {
                            'input': '$comments',
                            'as': 'c',
                            'cond': {'$not': '$$c.deleted'}
                        }
                    }
                }
            }
        }

        # check if size is 0 then set it to maximum (limit can not be 0)
        size = 999 if size == 0 else size

        # fetch list
        cur = self._collection.aggregate([
            condition,
            projection,
            # skip first
            {'$skip': offset},
            # keep order after skip
            {'$limit': size}
        ])

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
        condition = {'$match': {'_id': ObjectId(article_id), 'deleted': False}}

        # update views first
        updated = self._collection.update_one(
            condition,
            {'$inc': {'views': 1}}
        )

        # if no matched article
        if updated.modified_count == 0:
            raise NoSuchArticleError('No such article.')

        # format
        projection = {
            '$project': {
                '_id': 1,
                'title': 1,
                'author': 1,
                'content': 1,
                'views': 1,
                'tags': 1,
                'timestamp': 1,
                'reviews': {
                    '$size': {
                        '$filter': {
                            'input': '$comments',
                            'as': 'c',
                            'cond': {'$not': '$$c.deleted'}
                        }
                    }
                },
                'comments': {
                    '$slice': [
                        {
                            '$filter': {
                                'input': '$comments',
                                'as': 'c',
                                'cond': {'$not': '$$c.deleted'}
                            }
                        },
                        comments_size
                    ]
                }
            }
        }

        # fetch document
        data = self._collection.aggregate([condition, projection])

        # put result into list, it should be only one element if succeed
        result = [x for x in data]

        # if nothing was fetched raise error
        if len(result) == 0:
            raise NoSuchArticleError('No such article.')

        # deal with ObjectId and return the first element
        return deal_with_object_id(result)[0]

    def get_comments(self, article_id, *, size, offset, fetch_deleted=False):
        """Get article content

        :param article_id: article ID
        :param size: fetch size
        :param offset: skip
        :param fetch_deleted: fetch deleted object flag, only admin can set to True
        :raise: 404 NoSuchArticleError
        :return: array of comments, count
        """

        # check if size is 0 then set it to maximum (limit can not be 0)
        size = 999 if size == 0 else size

        data = self._collection.aggregate([
            # unwind comment array
            {'$unwind': '$comments'},
            # match condition
            {'$match': {
                '_id': ObjectId(article_id),
                'comments.deleted': False if not fetch_deleted else True
            }},
            # group date and calculate count
            {'$group': {
                '_id': '$_id',
                'count': {'$sum': 1},
                'comments': {
                    '$push': '$comments'
                }
            }},
            # only fetch comments
            {'$project': {
                'count': 1,
                'comments': {'$slice': ['$comments', offset, size]},
            }},
        ])

        # get result
        result = [x for x in data]

        # check result
        if len(result) == 0:
            raise NoSuchArticleError('No such articles.')

        # deal with ObjectId and return
        return deal_with_object_id(result[0]['comments']), result[0]['count']

    def post_comment(self, article_id, *, data):
        """Post new comment

        Post data should be checked before this method called.

        :param article_id: article ID
        :param data: comment data
        :raise: 404 NoSuchArticleError
        """

        # generate new comment ID
        data['cid'] = ObjectId()
        # set article ID to comment
        data['aid'] = ObjectId(article_id)
        # initial deleted flag
        data['deleted'] = False

        # execute update to push new comment
        result = self._collection.update_one(
            {'_id': ObjectId(article_id)},
            {'$push': {'comments': data}}
        )

        # check result
        if result.modified_count == 0:
            raise NoSuchArticleError('No such article.')

    def delete_comment(self, article_id, comment_id):
        """Delete a comment

        :param article_id: article ID
        :param comment_id: comment ID
        :raises:
            - 404 NoSuchArticleOrCommentError
        """
        # update
        r = self._collection.update_one(
            # match specified article and comment
            {
                '_id': ObjectId(article_id),
                'comments': {
                    '$elemMatch': {
                        'cid': ObjectId(comment_id),
                        'deleted': False
                    }
                }
            },
            # soft delete
            {
                '$set': {
                    'comments.$.deleted': True,
                    'comments.$.deleted_time': get_current_time_in_milliseconds()
                }
            }
        )

        # if there is nothing matched
        if r.matched_count == 0:
            raise NoSuchArticleOrCommentError('No such article or comment.')

    def get_articles_counts(self):
        """Get articles count

        :return: counts of articles
        """
        return self._collection.count({'deleted': False})
