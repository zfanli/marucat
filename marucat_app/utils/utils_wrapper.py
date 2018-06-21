#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""High order utils"""
from marucat_app.utils.utils import (
    create_error_message,
    convert_to_number, is_positive_number
)


def not_a_number(name):
    """Create a error message describe the variable is not a number.

    Message
        Invalid query parameters. {Variable name} must be a number.

    :param name: variable name
    :return: error message dict
    """
    return create_error_message(
        'Invalid query parameters. {} must be a number.'.format(
            name
        )
    )


def not_a_positive_number(name):
    """Create a error message describe the variable is not a positive number.

    Message
        Invalid query parameters. {Variable name} must be a positive number.

    :param name: variable name
    :return: error message dict
    """
    return create_error_message(
        'Invalid query parameters. {} must be a positive number.'.format(
            name
        )
    )


def no_such_article():
    """Create a error message describe the article does not exist.

     Message
        Specified article does not exist.

    :return: error message dict
    """
    return create_error_message('Specified article does not exist.')


def articles_list_not_found(tags):
    """Create a error message describe the articles list is None.

    Message
        Can not found any articles. (if tags is None)
        Can not found any articles tagged by {tags}. (if tags is not None)

    :param tags: tags
    :return: error message dict
    """
    message = 'Can not found any articles{}.'.format(
        ' tagged by {}'.format(tags) if tags is not None else ''
    )
    return create_error_message(message)


def convert_and_check_positive_number(*arr):
    """Convert and check whether the elements of target array are all
        positive number or not.

    :param arr: target array
    :return: result of convert
    """

    c = convert_to_number(*arr)
    if is_positive_number(*c):
        return c
    raise ValueError('Target must be a positive number.')