#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utils"""

import re

from marucat_app.utils.errors import NotANumberError

APP_NAME = 'marucat_app'
CONNECTOR_FACTORY = 'connector_factory'


def get_db_helper(app, name):
    """Get helper from connector

    :param app: current app instance
    :param name: the name of helper, usually end with '_connector'
    """
    c = app.config[CONNECTOR_FACTORY]
    return getattr(c, name)


def create_error_message(message='Error was happened.'):
    """Create a error message dict for JSON

    :param message: error message
    :return: dict contain a error message
    """
    return {'error': message}


def convert_to_number(*arr):
    """Convert all elements of the arr to number

    :param arr: array of elements which will be converted to number
    :return the result of conversion

    Raise a NotANumber error when a element cannot convert to number.
    """
    r = []
    try:
        for i in range(len(arr)):
            r.append(int(arr[i]))
    except ValueError:
        raise NotANumberError(
            'Parameters contains a element which is not a number.'
        )

    # there is no error so just return the result
    return r


def is_positive_number(*arr):
    """Check is the number a positive number.

    :param arr: number array
    :return: True if it is a positive number, or False if not
    """
    for n in arr:
        if n <= 0:
            return False
    return True


def has_special_characters(target):
    """Check whether the target strings contained a special characters or not.

    Definition of special characters
        `~!@#$%^&*()=_-+<>?:"{},./;'[]

    :param target: test strings
    :return: True if contained or False if not
    """
    pattern = r'[`~!@#$%^&*()=_\-\+<>?:"{},./;\'\[\]]'
    return bool(re.search(pattern, target))


def convert_string_to_list(target):
    """Convert string to array

    :param target: target string
    :return: result list if convert succeeded or origin string if not
    """
    pattern = r'^\[.*\]$'
    # surround with '[]'?
    if re.search(pattern, target):
        content = target[1:-1]
        # contained special characters?
        if not has_special_characters(content):
            return content.split(',')
    # cannot convert just return origin string
    return target


if __name__ == '__main__':
    pass