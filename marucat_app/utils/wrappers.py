#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""High order utils"""
from marucat_app.utils.utils import (
    convert_to_number, is_positive_number,
    is_natural_number
)


def convert_and_check_positive_number(*arr):
    """Convert and check the parameters

    Try to convert all of the parameters to number,
    and check if they are positive number.

    :param arr: target list
    :return: result of convert
    """

    c = convert_to_number(*arr)
    if is_positive_number(*c):
        return c
    raise ValueError('Target must be a positive number.')


def convert_and_check_natural_number(*arr):
    """Convert and check the parameters

    Try to convert all of the parameters to number,
    and check if they are natural number (includes zero).

    :param arr: target list
    :return: a list contains all of results,
            note if only one result is expected, use `[var]` to receive it
    """

    c = convert_to_number(*arr)
    if is_natural_number(*c):
        return c
    raise ValueError('Target must be a natural number (includes zero).')
