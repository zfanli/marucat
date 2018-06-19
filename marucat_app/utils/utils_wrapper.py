#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""High order utils"""
from marucat_app.utils.utils import create_error_message
from utils.utils import convert_to_number, is_positive_number


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


def convert_and_check_positive_number(*arr):
    """First convert the target to number and check is it a positive number."""

    c = convert_to_number(*arr)
    if is_positive_number(*c):
        return c
    raise ValueError('Target must be a positive number.')
