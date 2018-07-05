#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Blueprint of articles"""

from flask import Blueprint, current_app, jsonify, request

from marucat_app.utils import errors
from marucat_app.utils import utils
from marucat_app.utils import utils_wrapper

# handling the url start with '/articles'
bp = Blueprint('articles', __name__, url_prefix='/articles')

# Articles' Database helper's key
ARTICLES_HELPER = 'articles_helper'


@bp.route('/', methods=['GET'])
def articles_list_fetch():
    """Fetch articles list

    Query parameters
        - size: number, fetch size, 10 by default
        - offset: number, fetch start position, 0 by default
        - tags: string or strings array, tags

    :return
        - 200 normally
        - 400 invalid query parameters
        - 404 not found
    """

    # get request parameters
    size = request.args.get('size', 10)
    offset = request.args.get('offset', 0)

    # try to convert parameters to number and do some check
    try:
        size, offset = utils_wrapper.convert_and_check_natural_number(size, offset)
    except errors.NotANumberError:
        # not a number
        error = utils_wrapper.not_a_number('size/offset')
        return jsonify(error), 400
    except ValueError:
        # not a positive number
        error = utils_wrapper.not_a_natural_number('size/offset')
        return jsonify(error), 400

    # get tags from request
    tags = request.args.get('tags')
    # convert tags to list if it is not a None
    if tags is not None:
        tags = utils.convert_string_to_list(tags)

    # get articles helper
    articles_helper = utils.get_db_helper(current_app, ARTICLES_HELPER)

    # fetch list
    a_list = articles_helper.get_list(size=size, offset=offset, tags=tags)

    # 404 not found
    if a_list is None or len(a_list) == 0:
        error = utils_wrapper.articles_list_not_found(tags, offset)
        return jsonify(error), 404

    # get all counts of articles
    all_counts = articles_helper.get_articles_counts()
    headers = {'next-page': True}
    if (all_counts - size - offset) <= 0:
        headers['next-page'] = False

    # pretty print if required or in debug mode
    pretty_flag = current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] or current_app.debug

    # 200
    return utils.create_response(headers, a_list, 200, pretty_flag)


@bp.route('/<article_id>', methods=['GET'])
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
    # convert and check
    try:
        [comments_size] = utils_wrapper.convert_and_check_natural_number(comments_size)
    except errors.NotANumberError:
        # not a number
        error = utils_wrapper.not_a_number('comments_size')
        return jsonify(error), 400
    except ValueError:
        # not a natural number
        error = utils_wrapper.not_a_natural_number('comments_size')
        return jsonify(error), 400

    # check if the article ID contains special characters
    if utils.has_special_characters(article_id):
        # 404
        error = utils_wrapper.no_such_article()
        return jsonify(error), 404

    articles_helper = utils.get_db_helper(current_app, ARTICLES_HELPER)

    # fetch content
    try:
        content = articles_helper.get_content(article_id, comments_size=comments_size)
    except errors.NoSuchArticleError:
        # 404
        error = utils_wrapper.no_such_article()
        return jsonify(error), 404

    # 200
    return jsonify(content), 200


@bp.route('/<article_id>/comments', methods=['GET'])
def article_comments_fetch(article_id):
    """Fetch article's comments by id

    Query parameters
        - size: number, fetch size
        - page: number, fetch start position

    :param article_id: article ID
    :return:
        - 200 normally
        - 400 invalid query parameters
        - 404 not found
    """

    # check is the provided article id contains a special characters or not
    if utils.has_special_characters(article_id):
        # 404
        error = utils_wrapper.no_such_article()
        return jsonify(error), 404

    size = request.args.get('size', 10)
    offset = request.args.get('offset', 0)

    # convert to number and checking
    try:
        size, offset = utils_wrapper.convert_and_check_natural_number(size, offset)
    except errors.NotANumberError:
        # not a number
        error = utils_wrapper.not_a_number('size/offset')
        return jsonify(error), 400
    except ValueError:
        # values <= 0
        error = utils_wrapper.not_a_positive_number('size/offset')
        return jsonify(error), 400

    articles_helper = utils.get_db_helper(current_app, ARTICLES_HELPER)

    # fetch comments
    try:
        comments = articles_helper.get_comments(
            article_id, size=size, offset=offset
        )
    except errors.NoSuchArticleError:
        # 404
        error = utils_wrapper.no_such_article()
        return jsonify(error), 404

    # 200
    return jsonify(comments), 200


@bp.route('/<article_id>/comments', methods=['POST'])
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

    # check if the article ID contains special characters
    if utils.has_special_characters(article_id):
        # 404
        error = utils_wrapper.no_such_article()
        return jsonify(error), 404

    # get post data
    data = request.get_json()
    # check attributes
    keys = ['from', 'body', 'timestamp']
    if not utils.is_contained(data, keys):
        error = utils_wrapper.invalid_post_data(keys)
        return jsonify(error), 400

    # get articles helper
    articles_helper = utils.get_db_helper(current_app, ARTICLES_HELPER)

    try:
        articles_helper.post_comment(article_id, data=data)
    except errors.NoSuchArticleError:
        error = utils_wrapper.no_such_article()
        return jsonify(error), 404

    return '', 201


@bp.route('/<article_id>/comments/<comment_id>', methods=['DELETE'])
def article_comments_delete(article_id, comment_id):
    """Delete specific comment

    :param article_id: article ID
    :param comment_id: comment ID
    """
    # check if the article ID contains special characters
    if utils.has_special_characters(article_id):
        # 404
        error = utils_wrapper.no_such_article()
        return jsonify(error), 404
    # check if the comment ID contains special characters
    if utils.has_special_characters(comment_id):
        # 404
        error = utils_wrapper.no_such_comment()
        return jsonify(error), 404

    # get articles helper
    articles_helper = utils.get_db_helper(current_app, ARTICLES_HELPER)

    try:
        articles_helper.delete_comment(article_id, comment_id)
    except errors.NoSuchArticleError:
        # 404
        error = utils_wrapper.no_such_article()
        return jsonify(error), 404
    except errors.NoSuchCommentError:
        # 404
        error = utils_wrapper.no_such_comment()
        return jsonify(error), 404

    # everything are going well
    return '', 200


# Pending api below.
# Those api might not be implemented.
# Just placeholders for now.

@bp.route('/<article_id>', methods=['PUT'])
def article_content_save(article_id):
    """Update article's content

    :param article_id: article ID
    """

    # TODO

    r = {'article_id': article_id, 'method': 'PUT'}
    return jsonify(r), 200


@bp.route('/<article_id>', methods=['POST'])
def article_content_create(article_id):
    """Create article

    :param article_id: article ID
    """

    # TODO

    r = {'article_id': article_id, 'method': 'POST'}
    return jsonify(r), 200


@bp.route('/<article_id>', methods=['DELETE'])
def article_content_delete(article_id):
    """Delete article

    :param article_id: article ID
    """

    # TODO

    r = {'article_id': article_id, 'method': 'DELETE'}
    return jsonify(r), 200
