#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Definition of runtime errors"""


class NoSuchArticleError(RuntimeError):
    pass


class DatabaseDoNotExistError(RuntimeError):
    pass


class NotANumberError(RuntimeError):
    pass
