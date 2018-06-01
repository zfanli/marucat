#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Integration"""

from flask import Blueprint
from marucat_app.marucat_utils import create_response
from marucat_app.db_connector import ConnectorCreator

bp = Blueprint('articles', __name__, url_prefix='/articles')
articles_helper = ConnectorCreator().articles_connector


@bp.route('/list')
def articles_list():
    """Get articles list"""
    a_list = articles_helper.get_list()
    resp = create_response(a_list, 200)
    return resp
