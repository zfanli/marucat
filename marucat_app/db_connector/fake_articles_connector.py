#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Description here"""

from json import dumps


def get_list():
    return dumps([{'id': 1, 'message': 'Hi'}, {'id': 2, 'message': 'Hello'}])


class ArticlesConnector(object):
    """A fake API for testing"""
    def __init__(self):
        self.get_list = get_list

