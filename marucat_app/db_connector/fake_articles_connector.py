#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Description here"""

from json import dumps


def get_list(*, size, page):
    return dumps([{'id': 1, 'size': size}, {'id': 2, 'page': page}])


class ArticlesConnector(object):
    """A fake API for testing"""
    def __init__(self):
        self.get_list = get_list
