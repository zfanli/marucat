#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Blueprint of articles"""

from flask import Blueprint, current_app, jsonify, request

from marucat_app.utils.errors import NoSuchArticleError, NotANumberError
from marucat_app.utils.utils import (
    get_db_helper, has_special_characters
)
from marucat_app.utils.utils_wrapper import convert_and_check_positive_number
from marucat_app.utils.utils_wrapper import (
    no_such_article, not_a_number,
    not_greater_than_zero
)

# handling the url start with '/articles'
bp = Blueprint('articles', __name__, url_prefix='/articles')

# the name of article's db helper
ARTICLES_HELPER = 'articles_connector'


@bp.route('/list', methods=['GET'])
def articles_list_fetch():
    """Fetch articles list

    Query parameters
        size: number, fetch size, 10 by default
        page: number, fetch start position, 1 by default
        tags: string or strings array, tags

    :return
        200 normally
        400 invalid query parameters
    """
    size = request.args.get('size', 10)
    page = request.args.get('page', 1)

    # convert to number and checking
    try:
        size, page = convert_and_check_positive_number(size, page)
    except NotANumberError:
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
    if has_special_characters(article_id):
        # 404
        error = no_such_article()
        return jsonify(error), 404

    articles_helper = get_db_helper(current_app, ARTICLES_HELPER)

    # fetch content
    try:
        content = articles_helper.get_content(article_id)
    except NoSuchArticleError:
        # 404
        error = no_such_article()
        return jsonify(error), 404

    # 200
    return jsonify(content), 200


@bp.route('/aid<article_id>/comments', methods=['GET'])
def article_comments_fetch(article_id):
    """Fetch article's comments by id

    Query parameters
        size: number, fetch size
        page: number, fetch start position

    :param article_id: article ID
    :return
        200 normally
        400 invalid query parameters
        404 article does not exist
    """

    # check is the provided article id contains a special characters or not
    if has_special_characters(article_id):
        # 404
        error = no_such_article()
        return jsonify(error), 404

    size = request.args.get('size', 10)
    page = request.args.get('page', 1)

    # convert to number and checking
    try:
        size, page = convert_and_check_positive_number(size, page)
    except NotANumberError:
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
    except NoSuchArticleError:
        # 404
        error = no_such_article()
        return jsonify(error), 404

    # 200
    return jsonify(comments), 200


@bp.route('/aid<article_id>/comments', methods=['POST'])
def article_comments_save(article_id):
    """Push comment

    :param article_id: article ID
    """

    # TODO

    print(article_id)
    data = request.get_json()
    return jsonify(data), 200


@bp.route('/aid<article_id>/comments/<comment_id>', methods=['DELETE'])
def article_comments_delete(article_id, comment_id):
    """Delete specific comment

    :param article_id: article ID
    :param comment_id: comment ID
    """

    # TODO

    r = {'article_id': article_id, 'comment_id': comment_id}
    return jsonify(r), 200


# Pending apis below.
# Those apis might not be implemented.
# Just placeholders for now.

@bp.route('/aid<article_id>', methods=['PUT'])
def article_content_save(article_id):
    """Update article's content

    :param article_id: article ID
    """

    # TODO

    r = {'article_id': article_id, 'method': 'PUT'}
    return jsonify(r), 200


@bp.route('/aid<article_id>', methods=['POST'])
def article_content_create(article_id):
    """Create article

    :param article_id: article ID
    """

    # TODO

    r = {'article_id': article_id, 'method': 'POST'}
    return jsonify(r), 200


@bp.route('/aid<article_id>', methods=['DELETE'])
def article_content_delete(article_id):
    """Delete article

    :param article_id: article ID
    """

    # TODO

    r = {'article_id': article_id, 'method': 'DELETE'}
    return jsonify(r), 200
