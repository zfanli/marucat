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

    def perform_test_whit_params(input_val, expect_val):
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
    perform_test_whit_params(None, default_val)

    # specific params
    # articles/list?size=55&page=999
    perform_test_whit_params((55, 999), (55, 999))

    # error checking
    # no val provided to size
    # articles/list?size=&page=998
    perform_test_whit_params(('', 998), (10, 998))

    # no val provided to page
    # articles/list?size=1098&page=
    perform_test_whit_params((1098, ''), (1098, 1))

    # no val provided to both
    # articles/list?size=&page=
    perform_test_whit_params(('', ''), default_val)

    # invalid val provided to size
    # articles/list?size=abc&page=192
    perform_test_whit_params(('abc', 192), (10, 192))

    # invalid val provided to size
    # articles/list?size=111&page=acb
    perform_test_whit_params((111, 'acb'), (111, 1))
