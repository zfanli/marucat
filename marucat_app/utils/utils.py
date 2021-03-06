#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utils"""

import re
import time
from os import path
from configparser import ConfigParser
from json import dumps

from bson import ObjectId
from flask import make_response

from marucat_app.utils.errors import NotANumberError

# App name
APP_NAME = 'marucat_app'
# Connector factory key
CONNECTOR_FACTORY = 'connector_factory'


def get_db_helper(app, name):
    """Get helper from connector

    :param app: current app instance
    :param name: the name of helper, usually end with '_connector'
    """
    c = app.config[CONNECTOR_FACTORY]
    return getattr(c, name)


def create_unimplemented_message(param, method):
    """Message to tell you request is succeed but requested API is unimplemented.

    :param param: request param
    :param method: request method
    :return: message object
    """
    date = {
        'message': 'Request is succeed, but this API is unimplemented.',
        'param': param,
        'method': method
    }
    return date


def convert_to_number(*arr):
    """Convert all elements of the arr to number

    :param arr: array of elements which will be converted to number
    :return: a list contains all the result,
            note if only one result is expected, use `[var]` to receives it

    Raise a NotANumber error when a element cannot convert to number.
    """
    r = []
    try:
        for i in arr:
            r.append(int(i))
    except ValueError:
        raise NotANumberError(
            'Parameters contains a element which is not a number.'
        )

    # there is no error so just return the result
    return r


def is_positive_number(*arr):
    """Check if the numbers are positive number.

    :param arr: number array
    :return: True if are positive number, or False if not
    """
    for n in arr:
        if n <= 0:
            return False
    return True


def is_natural_number(*arr):
    """Check if the numbers are natural number (includes zero).

    :param arr: number array
    :return: True if are natural number, or False if not
    """
    for n in arr:
        if n < 0:
            return False
    return True


def has_special_characters(target):
    """Check whether the target strings contained a special characters or not.

    Definition of special characters
        `~!@#$%^&*()=_-+<>?:"{},./;'[]\

    :param target: test strings
    :return: True if contained or False if not
    """
    pattern = r'[`~!@#$%^&*()=_\-\+<>?:"{},./;\'\[\]\\]'
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


def is_contained(target, keys):
    """Check is the target json object contained specified keys

    :param target: target json object
    :param keys: keys
    :return: True if all of keys contained or False if anyone is not contained
    Invalid parameters is always return False.
    """

    if not target or not keys:
        return False

    # if keys is just a string convert it to a list
    if type(keys) == str:
        keys = [keys]

    # traverse the list to check json object
    # if key does not exist or value is None then return False
    try:
        for key in keys:
            if target[key] is None:
                return False
    except KeyError:
        return False

    # All seems to be going well
    return True


def get_initial_file():
    """Get initial file's content

    :return: ini file instance
    """

    # edit path to config.ini base on current file path
    # current file path: ~/marucat/marucat_app/utils/utils.py
    # target file path: ~/marucat/config.ini
    p = path.abspath(__file__)
    p = path.dirname(p)
    p = path.split(p)[0]
    p = path.split(p)[0]
    p = path.join(p, 'config.ini')

    # init parser
    config = ConfigParser()
    # return ini instance
    config.read(p)
    config.sections()
    return config


def deal_with_object_id(target):
    """Deal with ObjectId in MongoDB documents.

    Convert ObjectId to str.

    :param target: target list or dict
    :return: result without ObjectId
    """

    def convert_object_id(tar):
        """Convert ObjectId

        Check if it contains ObjectId and convert ObjectId to str if it does

        :param tar: target
        :return: converted result
        """

        # check tar's type
        t = type(tar)
        if t == ObjectId:
            return str(t)
        elif t != dict:
            return tar

        # check all keys in tar (when the tar is a dict)
        for k in tar:
            # if the attribute is ObjectId convert it to str
            if isinstance(tar[k], ObjectId):
                tar[k] = str(tar[k])
            # if the attribute is a list, travel the dict and check all attributes
            elif isinstance(tar[k], list):
                tar[k] = deal_with_object_id(tar[k])

        return tar

    if isinstance(target, dict):
        return convert_object_id(target)
    elif isinstance(target, list):
        result = []

        for n in target:
            result.append(convert_object_id(n))

        return result


def get_current_time_in_milliseconds():
    """Get current time in milliseconds.

    Because JavaScript accepts a milliseconds timestamp.

    :return: current time in milliseconds
    """
    return time.time() * 1000


def create_response(headers, data, code, pretty_flag):
    """Create a response use given headers and data.

    :param headers: dict, setting headers
    :param data: pass to jsonify method
    :param code: int, status code
    :param pretty_flag: control pretty print or not
    :return: response
    """
    if not headers:
        headers = {}
    if not isinstance(headers, dict):
        raise ValueError('Headers should be a dict.')

    # set JSON MIME
    headers['Content-Type'] = 'application/json'

    # check if needs pretty print
    if pretty_flag:
        data = dumps(data, sort_keys=True, indent=2) + '\n'
    else:
        data = dumps(data)

    # return response
    return make_response(data, code, headers)


def isinstance_all(ins, *tar):
    """Apply isinstance() to all elements of target

    :param ins: types
    :param tar: target tuple
    :return: True if all True and False if anyone False
    """
    for x in tar:
        if not isinstance(x, ins):
            return False

    return True


def set_next_page_and_data(counts, size, offset, data, pretty_flag):
    """Deal with json data and headers

    - Calculate next-page and set to header
    - Set MIME to JSON type
    - Dump data and format it if necessary

    :param counts: counts
    :param size: size
    :param offset: offset
    :param data: pass to jsonify method
    :param pretty_flag: control pretty print or not
    :return: header, data
    """

    if not isinstance_all(int, size, offset, counts):
        raise ValueError('Headers should be a dict.')

    next_page = False

    if (counts - size - offset) > 0:
        next_page = True

    # set JSON MIME
    headers = {
        'Content-Type': 'application/json',
        'next-page': next_page
    }

    # check if needs pretty print
    if pretty_flag:
        data = dumps(data, sort_keys=True, indent=2) + '\n'
    else:
        data = dumps(data)

    # return response
    return headers, data


def filter_deleted_items(items, flag):
    """Filter deleted items

    :param items: target
    :param flag: deleted flag name, always True means deleted
    :return: list does not contain deleted items
    """

    # just return if parameter is not a list
    if not isinstance(items, list):
        return items

    result = filter(lambda x: not x[flag], items)
    return [x for x in result]


if __name__ == '__main__':
    pass
