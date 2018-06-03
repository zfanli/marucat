#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Description here"""

from flask import jsonify


def get_list(*, size, page):
    return jsonify([{'id': 1, 'size': size}, {'id': 2, 'page': page}])


def get_content(article_id):
    return jsonify({'id': article_id, 'content': 'The content of article.'})


class ArticlesConnector(object):
    """A fake API for testing"""
    def __init__(self):
        self.get_list = get_list
        self.get_content = get_content
