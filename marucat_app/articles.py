#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Integration"""

__author__ = 'Z.Rick'

from flask import Blueprint, current_app
from marucat_app.marucat_utils import create_response
from marucat_app.db_connector import ConnectorCreator

bp = Blueprint('articles', __name__, url_prefix='/articles')
articles_helper = ConnectorCreator(current_app.logger).articles_connector


@bp.route('/list')
def articles_list():
    a_list = articles_helper.get_lists()
    resp = create_response(a_list, 200)
    return resp
