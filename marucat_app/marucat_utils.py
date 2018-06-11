#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utils module for constants and common functions"""

import re
from marucat_app.errors import NotANumber

APP_NAME = 'marucat_app'
CONNECTOR_FACTORY = 'connector_factory'


def get_db_helper(app, name):
    """Get helper from connector

    :param app: current app instance
    :param name: the name of helper, usually end with '_connector'
    """
    c = app.config[CONNECTOR_FACTORY]
    return getattr(c, name)


# Creating messages

def create_error_message(message='Error was happened.'):
    """Create a error object(dict)"""
    return {'error': message}


def not_a_number(name):
    """Not a number error message"""
    return create_error_message(
        'Invalid query parameters. {} must be a number.'.format(
            name
        )
    )


def not_greater_than_zero(name):
    """Less than zero or equals to 0 error message"""
    return create_error_message(
        'Invalid query parameters. {} must be greater than 0.'.format(
            name
        )
    )


def no_such_article():
    """No such article"""
    return create_error_message('Specified article does not exists.')


# Conversion and checking utils

def convert_to_number(*arr):
    """Convert all elements of the arr to number

    :param arr: array of elements which will be converted to number
    :return the result of conversion

    Raise a NotANumber error when a element cannot convert to number.
    """
    r = [None for x in range(len(arr))]
    try:
        for i in range(len(arr)):
            r[i] = int(arr[i])
    except ValueError:
        raise NotANumber(
            'Parameters contains a element which is not a number.'
        )

    # there is no error so just return the result
    return r


def check_number_greater_than_zero(*arr):
    for n in arr:
        if n <= 0:
            raise ValueError('Number must be greater than 0.')


def convert_and_check_number_gt_zero(*arr):
    c = convert_to_number(*arr)
    check_number_greater_than_zero(*c)
    return c


def is_special_characters_contained(target):
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
        except NotANumber as e:
            msg = 'Parameters contains a element which is not a number.'
            assert e.__str__() == msg

    convert_error('a')
    convert_error('123', 'a')

    assert not is_special_characters_contained('T123')
