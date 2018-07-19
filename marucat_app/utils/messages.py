#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def create_error_message(message='Error was happened.'):
    """Create a error message dict for JSON

    :param message: error message
    :return: dict contain a error message
    """
    return {'error': message}


def not_a_number(name):
    """Create a error message describe the variable is not a number.

    Message
        Invalid query parameters. {Variable name} must be a number.

    :param name: variable name
    :return: error message dict
    """
    return create_error_message(
        'Invalid query parameters. {} must be a number.'.format(
            name
        )
    )


def not_a_positive_number(name):
    """Create a error message describe the variable is not a positive number.

    Message
        Invalid query parameters. {Variable name} must be a positive number.

    :param name: variable name
    :return: error message dict
    """
    return create_error_message(
        'Invalid query parameters. {} must be a positive number.'.format(
            name
        )
    )


def not_a_natural_number(name):
    """Create a error message describe the variable is not a natural number.

    Message
        Invalid query parameters. {Variable name} must be a natural number.

    :param name: variable name
    :return: error message dict
    """
    return create_error_message(
        'Invalid query parameters. {} must be a natural number.'.format(
            name
        )
    )


def no_such_article():
    """Create a error message describe the article does not exist.

     Message
        Specified article does not exist.

    :return: error message dict
    """
    return create_error_message('Specified article does not exist.')


def no_such_article_or_comment():
    """Create a error message describe that the article or comment does not exist.

     Message
        Specified article or comment does not exist.

    :return: error message dict
    """
    return create_error_message('Specified article or comment does not exist.')


def invalid_post_data(keys):
    """Create a error message describe the post data is invalid.

     Message
        Specified article does not exist.

    :return: error message dict
    """
    return create_error_message(
        'Invalid post data. '
        'The data should be a json object and contained these attributes: {}'.format(
            keys
        )
    )


def articles_list_not_found(tags, offset):
    """Create a error message describe the articles list is None.

    Message
        - Can not found any articles. (if tags is None)
        - Can not found any articles tagged by {tags}. (if tags is not None)

    :param tags: tags
    :param offset: offset
    :return: error message dict
    """
    message = 'Can not found any articles{}, offset {}.'.format(
        ' tagged by {}'.format(tags) if tags is not None else '',
        offset
    )
    return create_error_message(message)
