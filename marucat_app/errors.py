#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Definition of runtime errors"""


class NoSuchArticle(RuntimeError):
    pass


class DatabaseDoNotExist(RuntimeError):
    pass


class NotANumber(RuntimeError):
    pass
