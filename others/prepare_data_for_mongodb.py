#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Prepare some data for development or testing."""
import time

from pymongo import MongoClient

from marucat_app.utils.utils import get_initial_file, get_current_time_in_milliseconds


def get_articles_collection():
    conf = get_initial_file()
    mongo_conf = conf['mongodb']
    url = mongo_conf['url']
    port = int(mongo_conf['port'])
    schema = mongo_conf['schema']
    articles_collection = mongo_conf['articles_collection']

    mc = MongoClient(url, port)
    db = mc[schema]
    return db[articles_collection]


def make_data(aid, peek, content, views, tags, cid, comment, timestamp):

    return {
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
        'comments': [
            {
                # Article ID
                'aid': aid,
                # Comment ID
                'cid': cid,
                # Who wrote the comment
                'from': 'Mary',
                # Comment body
                'body': comment,
                # Created or updated timestamp
                'timestamp': timestamp,
                # Deleted flag
                'deleted': False
            },
            # ...
        ],
        # Created or updated timestamp
        'timestamp': timestamp,
        # Deleted flag
        'deleted': False
    }


if __name__ == '__main__':
    articles = get_articles_collection()
    data = make_data('as123456', 'Just a peek at there.', 'Nothing here',
                     998, 'OK', 'c123455', 'No comment', get_current_time_in_milliseconds())
    articles.delete_many({})
    articles.insert_one(data)
