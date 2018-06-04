#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Integration"""

from flask import Blueprint, request, jsonify
from marucat_app.db_connector import ConnectorCreator

bp = Blueprint('articles', __name__, url_prefix='/articles')
articles_helper = ConnectorCreator().articles_connector


@bp.route('/list', methods=['GET'])
def articles_list():
    """Get a list of articles

    Query parameters
        size: the size of list
        page: the required start position

    Request without query parameters will use the default value,
    the request of GET /articles/list,
    equals to GET /articles/list?size=10&page=1
    """
    size = request.args.get('size', 10, int)
    page = request.args.get('page', 1, int)
    a_list = articles_helper.get_list(size=size, page=page)
    return jsonify(a_list), 200


@bp.route('/aid<article_id>', methods=['GET'])
def article_content(article_id):
    """Get the content of article by id
    :param article_id: the id of article
    """
    content = articles_helper.get_content(article_id)
    views = articles_helper.increase_views(article_id)
    return jsonify(**content, **views), 200
