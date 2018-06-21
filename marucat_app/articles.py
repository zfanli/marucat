#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Blueprint of articles"""

from flask import Blueprint, current_app, jsonify, request

from marucat_app.utils.errors import NoSuchArticleError, NotANumberError
from marucat_app.utils.utils import (
    get_db_helper, has_special_characters,
    convert_string_to_list, is_contained
)
from marucat_app.utils.utils_wrapper import (
    convert_and_check_positive_number,
    no_such_article, not_a_number,
    not_a_positive_number, invalid_post_data,
    articles_list_not_found
)

# handling the url start with '/articles'
bp = Blueprint('articles', __name__, url_prefix='/articles')

# Articles' Database helper's key
ARTICLES_HELPER = 'articles_helper'


@bp.route('/list', methods=['GET'])
def articles_list_fetch():
    """Fetch articles list

    Query parameters
        - size: number, fetch size, 10 by default
        - page: number, fetch start position, 1 by default
        - tags: string or strings array, tags

    :return
        - 200 normally
        - 400 invalid query parameters
        - 404 not found
    """

    # get parameters from request
    size = request.args.get('size', 10)
    page = request.args.get('page', 1)

    # convert to number and check parameters
    try:
        size, page = convert_and_check_positive_number(size, page)
    except NotANumberError:
        # not a number
        error = not_a_number('size/page')
        return jsonify(error), 400
    except ValueError:
        # not a positive number
        error = not_a_positive_number('size/page')
        return jsonify(error), 400

    # get tags from request
    tags = request.args.get('tags')
    # convert tags to list when it is not a None
    if tags is not None:
        tags = convert_string_to_list(tags)

    # get articles helper
    articles_helper = get_db_helper(current_app, ARTICLES_HELPER)

    # fetch list
    a_list = articles_helper.get_list(size=size, page=page, tags=tags)

    # if nothing was found raise 404 error
    if a_list is None:
        error = articles_list_not_found(tags)
        return jsonify(error), 404

    # 200
    return jsonify(a_list), 200


@bp.route('/aid<article_id>', methods=['GET'])
def article_content(article_id):
    """Fetch article's content by id

    Query parameter
        comment_sizes: number, fetch comments size

    :param article_id: string, the id of article
    :return:
        - 200 normally
        - 400 invalid query parameter
        - 404 not found
    """

    # get comments size
    comments_size = request.args.get('comments_size', 10)
    # convert and check number
    try:
        comments_size = convert_and_check_positive_number(comments_size)
    except NotANumberError:
        # not a number
        error = not_a_number('comments_size')
        return jsonify(error), 400
    except ValueError:
        # not a positive number
        error = not_a_positive_number('comments_size')
        return jsonify(error), 400

    # check is the provided article id contains a special characters or not
    if has_special_characters(article_id):
        # 404
        error = no_such_article()
        return jsonify(error), 404

    articles_helper = get_db_helper(current_app, ARTICLES_HELPER)

    # fetch content
    try:
        content = articles_helper.get_content(article_id, comments_size=comments_size)
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
        - size: number, fetch size
        - page: number, fetch start position

    :param article_id: article ID
    :return:
        - 200 normally
        - 400 invalid query parameters
        - 404 article does not exist
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
        error = not_a_positive_number('size/page')
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

    The request's content-type should be **application/json**

    Post Data
        - from: from user
        - body: body of comment
        - reply_id: comment ID for reply to, *not necessary*
        - timestamp: created or updated timestamp

    :param article_id: article ID
    """

    # TODO

    print(article_id)

    # get post data
    data = request.get_json()
    # check attributes
    keys = ['from', 'body', 'timestamp']
    if not is_contained(data, keys):
        error = invalid_post_data(keys)
        return jsonify(error), 400

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


# Pending api below.
# Those api might not be implemented.
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
