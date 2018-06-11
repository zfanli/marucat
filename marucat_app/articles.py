#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Blueprint of articles"""

from flask import Blueprint, request, jsonify, current_app
from marucat_app.errors import NoSuchArticle, NotANumber
from marucat_app.marucat_utils import (
    get_db_helper, not_a_number, not_greater_than_zero,
    no_such_article, is_special_characters_contained,
    convert_and_check_number_gt_zero
)

# handling the url start with '/articles'
bp = Blueprint('articles', __name__, url_prefix='/articles')

# the name of article's db helper
ARTICLES_HELPER = 'articles_connector'


@bp.route('/list', methods=['GET'])
def articles_list_fetch():
    """Fetch articles list

    Query parameters
        size: number, fetch size
        page: number, fetch start position

    Request without query parameters will use the default value,
    the request of GET /articles/list,
    equals to GET /articles/list?size=10&page=1

    :return
        200 normally
        400 invalid query parameters
    """
    size = request.args.get('size', 10)
    page = request.args.get('page', 1)

    # convert to number and checking
    try:
        size, page = convert_and_check_number_gt_zero(size, page)
    except NotANumber:
        # not a number
        error = not_a_number('size/page')
        return jsonify(error), 400
    except ValueError:
        # values <= 0
        error = not_greater_than_zero('size/page')
        return jsonify(error), 400

    articles_helper = get_db_helper(current_app, ARTICLES_HELPER)

    # fetch list
    a_list = articles_helper.get_list(size=size, page=page)

    # 200
    return jsonify(a_list), 200


@bp.route('/aid<article_id>', methods=['GET'])
def article_content(article_id):
    """Fetch article's content by id

    :param article_id: string, the id of article
    :return
        200 normally
        404 article does not exist
    """

    # check is the provided article id contains a special characters or not
    if is_special_characters_contained(article_id):
        # 404
        error = no_such_article()
        return jsonify(error), 404

    articles_helper = get_db_helper(current_app, ARTICLES_HELPER)

    # fetch content
    try:
        content = articles_helper.get_content(article_id)
        views = articles_helper.update_views(article_id)
    except NoSuchArticle:
        # 404
        error = no_such_article()
        return jsonify(error), 404

    # 200
    return jsonify(**content, **views), 200


@bp.route('/aid<article_id>/comments', methods=['GET'])
def article_comments_fetch(article_id):
    """Fetch article's comments by id

    Query parameters
        size: number, fetch size
        page: number, fetch start position

    :param article_id: identity of article
    :return
        200 normally
        400 invalid query parameters
        404 article does not exist
    """

    # check is the provided article id contains a special characters or not
    if is_special_characters_contained(article_id):
        # 404
        error = no_such_article()
        return jsonify(error), 404

    size = request.args.get('size', 10)
    page = request.args.get('page', 1)

    # convert to number and checking
    try:
        size, page = convert_and_check_number_gt_zero(size, page)
    except NotANumber:
        # not a number
        error = not_a_number('size/page')
        return jsonify(error), 400
    except ValueError:
        # values <= 0
        error = not_greater_than_zero('size/page')
        return jsonify(error), 400

    articles_helper = get_db_helper(current_app, ARTICLES_HELPER)

    # fetch comments
    try:
        comments = articles_helper.get_comments(
            article_id, size=size, page=page
        )
    except NoSuchArticle:
        # 404
        error = no_such_article()
        return jsonify(error), 404

    # 200
    return jsonify(comments), 200


@bp.route('/aid<article_id>/comments', methods=['POST'])
def article_comments_save(article_id):
    """Submit comments

    :param article_id: indentity of article
    """
    data = request.get_json()
    return jsonify(data), 200
