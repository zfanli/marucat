#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Unit tests about API of articles"""

import pytest
import json
from logging import DEBUG
from marucat_app import create_app


@pytest.fixture
def client():
    app = create_app(level=DEBUG)
    app.testing = True
    return app.test_client()


def test_get_list(client):
    """get articles list"""

    def perform_get_list(input_val, expect_val):
        """test template"""
        # get inputted size and page
        size, page = input_val if input_val else (None, None)
        # get expected size and page
        e_size, e_page = expect_val

        # make request with query params
        # example: /articles/list?size=10&page=1
        requested_url = '/articles/list{}'.format(
            '?{}{}{}'.format(
                'size={}'.format(size) if size else '',
                '&' if size and page else '',
                'page={}'.format(page) if page else ''
            ) if size or page else ''
        )

        # print(requested_url)

        # perform request
        rv = client.get(requested_url)

        # check return code
        assert 200 == rv.status_code
        # check Content-Type
        assert 'application/json' == rv.content_type
        # check data
        assert [{'id': 1, 'size': e_size}, {'id': 2, 'page': e_page}] == json.loads(rv.data)

    # default values (size, page)
    default_val = (10, 1)

    # default params
    # articles/list
    perform_get_list(None, default_val)

    # specific params
    # articles/list?size=55&page=999
    perform_get_list((55, 999), (55, 999))

    # error checking
    # no val provided to size
    # articles/list?size=&page=998
    perform_get_list(('', 998), (10, 998))

    # no val provided to page
    # articles/list?size=1098&page=
    perform_get_list((1098, ''), (1098, 1))

    # no val provided to both
    # articles/list?size=&page=
    perform_get_list(('', ''), default_val)

    # invalid val provided to size
    # articles/list?size=abc&page=192
    perform_get_list(('abc', 192), (10, 192))

    # invalid val provided to size
    # articles/list?size=111&page=acb
    perform_get_list((111, 'acb'), (111, 1))


def test_get_content(client):

    def perform_get_content(article_id):
        rv = client.get('/article/aid{}'.format(article_id))
        assert 200 == rv.status_code
