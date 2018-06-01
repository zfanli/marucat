#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Description here"""

__author__ = 'Z.Rick'

from json import dumps


def get_lists():
    return dumps([{'id': 1, 'message': 'Hi'}, {'id': 2, 'message': 'Hello'}])


class ArticlesConnector(object):
    """A fake API for testing"""
    def __init__(self):
        self.get_lists = get_lists

