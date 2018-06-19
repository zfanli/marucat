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
    """Create a error object(dict)"""
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
    """Check is the numbers a natural number, just mean is it greater than 0."""
    for n in arr:
        if n <= 0:
            return False
    return True


def has_special_characters(target):
    """Check if the string contains a special characters list below"""
    pattern = r'[`~!@#$%^&*()=_\-\+<>?:"{},./;\'\[\]]'
    return bool(re.search(pattern, target))


if __name__ == '__main__':
    # test of create_error_message
    assert {'error': 'TEST'} == create_error_message('TEST')
    assert {'error': ''} == create_error_message('')
    assert {'error': 'Error was happened.'} == create_error_message()

    # test of convert_to_number
    assert [1, 2] == convert_to_number('1', '2')

    def convert_error(*arr):
        try:
            convert_to_number(*arr)
            raise AssertionError('Function do not work.')
        except NotANumberError as e:
            msg = 'Parameters contains a element which is not a number.'
            assert e.__str__() == msg

    convert_error('a')
    convert_error('123', 'a')

    assert not has_special_characters('T123')
