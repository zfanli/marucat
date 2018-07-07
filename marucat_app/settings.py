#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Global settings."""

from flask import Blueprint, jsonify, request

# handling the url start with '/articles'
bp = Blueprint('settings', __name__, url_prefix='/settings')

# Database helper key
SETTINGS_HELPER = 'settings_helper'


@bp.route('/', methods=['GET'])
def get_settings():
    """Fetch settings list

    :return: settings list
    """

    # TODO

    data = [
        {'name': 'test', 'value': 'v2'},
        {'name': 'test1', 'value': 'v3'},
    ]
    return jsonify(data), 200


@bp.route('/<name>', methods=['PUT'])
def update_settings(name):
    """Update settings

    :param name: setting's identifier
    :return:
    """
    # TODO
    return name + '\n'


@bp.route('/', methods=['POST'])
def create_settings():
    """Create settings

    Request's MIME should be application/json type.

    :return: created settings
    """
    # TODO
    return request.get_json()


@bp.route('/<name>', methods=['DELETE'])
def delete_settings(name):
    """Delete settings

    :param name: setting's identifier
    :return: delete result
    """
    # TODO
    return name + '\n'
