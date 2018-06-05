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

        rv = client.get(requested_url)
        assert 200 == rv.status_code
        assert [{'id': 1, 'size': e_size}, {'id': 2, 'page': e_page}] == json.loads(rv.data)

    # default values (size, page)
    default_val = (10, 1)

    # default params
    perform_test_whit_params((), default_val)

    # specific params
    perform_test_whit_params((55, 999), (55, 999))

    # error checking
    # no val provided to size
    perform_test_whit_params(('', 998), (10, 998))

    # no val provided to page
    perform_test_whit_params((1098, ''), (1098, 1))

    # no val provided to both
    perform_test_whit_params(('', ''), default_val)

    # invalid val provided to size
    perform_test_whit_params(('abc', 192), (10, 192))

    # invalid val provided to size
    perform_test_whit_params((111, 'acb'), (111, 1))
