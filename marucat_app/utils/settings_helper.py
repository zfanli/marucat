#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Settings helper"""

from marucat_app.utils.utils import get_db_helper


def get_settings(name, app):
    """Get specified settings' value

    :param name: name
    :param app: current instance of app
    :return: the value of settings
    """
    if not isinstance(name, str):
        return

    helper = get_db_helper(app, 'settings_helper')
    result = helper.get_one(name)

    if not result:
        return

    return result['value']
