#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Integration"""

from flask import Blueprint, request, jsonify, current_app
from marucat_app.db_connector import ConnectorCreator
from marucat_app.marucat_utils import create_error_message
from marucat_app.runtime_errors import NoSuchArticle

bp = Blueprint('articles', __name__, url_prefix='/articles')


@bp.route('/list', methods=['GET'])
def articles_list():
    """Get a list of articles

    Query parameters
        size: number, the size of list
        page: number, the required start position

    Request without query parameters will use the default value,
    the request of GET /articles/list,
    equals to GET /articles/list?size=10&page=1

    If the params are invalid, the default values will be returned.
    """
    size = request.args.get('size', 10)
    page = request.args.get('page', 1)

    # parameters checking
    # if size or page is not a number, then return 400
    try:
        size = int(size)
        page = int(page)
    except ValueError:
        error = create_error_message('Invalid query parameters. size/page must be a number.')
        return jsonify(error), 400

    # if size or page is less than or equals to 0, then return 400
    if size <= 0 or page <= 0:
        error = create_error_message('Invalid query parameters. size/page must be greater than 0.')
        return jsonify(error), 400

    articles_helper = g.articles_helper
    a_list = articles_helper.get_list(size=size, page=page)
    return jsonify(a_list), 200


@bp.route('/aid<article_id>', methods=['GET'])
def article_content(article_id):
    """Get the content of article by id

    This api will get content, views, comments of the specific article

    :param article_id: string, the id of article
    """

    articles_helper = ConnectorCreator(current_app.config['db']).articles_connector
    try:
        content = articles_helper.get_content(article_id)
        views = articles_helper.update_views(article_id)
    except NoSuchArticle:
        error = create_error_message('Specified article does not exists.')
        return jsonify(error), 404
    return jsonify(**content, **views), 200


@bp.route('/aid<article_id>/comments')
def article_comments(article_id):
    """get comments of specific article

    :param article_id: identity of article
    """
    size = request.args.get('size', 10, int)
    page = request.args.get('page', 1, int)

    articles_helper = g.articles_helper
    comments = articles_helper.get_comments(article_id, size)
    return jsonify(comments), 200
