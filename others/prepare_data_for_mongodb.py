#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Prepare some data for development or testing."""

from pymongo import MongoClient
from bson import ObjectId

from marucat_app.utils.utils import get_initial_file, get_current_time_in_milliseconds


def get_connection():
    conf = get_initial_file()
    mongo_conf = conf['mongodb']
    url = mongo_conf['url']
    port = int(mongo_conf['port'])
    schema = mongo_conf['schema']
    mc = MongoClient(url, port)
    db = mc[schema]
    return db


def get_articles_collection(connection):
    conf = get_initial_file()
    mongo_conf = conf['mongodb']
    articles_collection = mongo_conf['articles_collection']

    return connection[articles_collection]


def get_settings_collection(connection):
    conf = get_initial_file()
    mongo_conf = conf['mongodb']
    settings_collection = mongo_conf['settings_collection']

    return connection[settings_collection]


def make_data(peek, content, views, tags, comment, timestamp):

    return {
        'title': 'The article title',
        # Author
        'author': 'Richard',
        # Peek or abstract
        'peek': peek,
        # Full content
        'content': content,
        # Counts of views
        'views': views,
        # Tags
        'tags': tags,
        # Comments
        'comments': comment,
        # Created or updated timestamp
        'timestamp': timestamp,
        # Deleted flag
        'deleted': False
    }


def make_comment(aid, cid, body, timestamp, deleted):

    return {
        # Article ID
        'aid': aid,
        # Comment ID
        'cid': cid,
        # Who wrote the comment
        'from': 'Mary',
        # Comment body
        'body': body,
        # Created or updated timestamp
        'timestamp': timestamp,
        # Deleted flag
        'deleted': deleted
    }


def make_settings():
    d = [
        {
            'name': 'max_size',
            'value': 999,
            'description': {
                'en': 'Maximum size for once request.'
            }
        },
        {
            'name': 'default_size',
            'value': 10,
            'description': {
                'en': 'Default size.'
            }
        },
    ]

    for n in d:
        n['updated_time'] = get_current_time_in_milliseconds()
        n['created_time'] = get_current_time_in_milliseconds()
        n['updated_by'] = 'Richard'

    return d


if __name__ == '__main__':
    c = get_connection()
    articles = get_articles_collection(c)
    data = make_data('Just a peek at there.', 'Nothing here',
                     998, ['OK', 'red', 'blue'], None, get_current_time_in_milliseconds())
    articles.delete_many({})
    rid = articles.insert_one(data)

    comments = list(map(lambda x: make_comment(
        rid.inserted_id, ObjectId(), 'Just comment for {}'.format(x),
        get_current_time_in_milliseconds(), False if x % 3 != 1 else True), range(8)))

    re = articles.update({'_id': rid.inserted_id}, {'$set': {'comments': comments}})

    settings = get_settings_collection(c)
    settings.delete_many({})
    se = make_settings()
    settings.insert_many(se)
