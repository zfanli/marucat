#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Unit tests about API of articles"""

import pytest
import json
from logging import DEBUG
from marucat_app import create_app


@pytest.fixture
def client():
    app = create_app(level=DEBUG, db='test')
    app.testing = True
    return app.test_client()


def test_get_list(client):
    """get articles list"""

    def perform_get_list(input_val, expect_val, code=200):
        """test template

        :param input_val: inputted values (size, page)
        :param expect_val: the expected result (size, page)
        :param code: expected status code
        """
        # get inputted size and page
        size, page = input_val if input_val else (None, None)

        # make request with query params
        # example: /articles/list?size=10&page=1
        requested_url = '/articles/list{}'.format(
            '?{}{}{}'.format(
                'size={}'.format(size) if size != '' else '',
                '&' if size and page else '',
                'page={}'.format(page) if page != '' else ''
            ) if size or page else ''
        )

        # perform request
        rv = client.get(requested_url)

        print(requested_url, rv.status_code)

        # check return code
        assert code == rv.status_code

        if 200 == code:
            # get expected size and page
            e_size, e_page = expect_val
            # check Content-Type
            assert 'application/json' == rv.content_type
            # check data
            assert [{'id': 1, 'size': e_size}, {'id': 2, 'page': e_page}] == json.loads(rv.data)
        elif 400 == code:
            assert rv.data is not None
            assert json.loads(rv.data)['error'] is not None

    # 200 below

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

    # 400 below

    # invalid val provided to size
    # articles/list?size=abc&page=192
    perform_get_list(('abc', 192), None, 400)

    # invalid val provided to size
    # articles/list?size=111&page=acb
    perform_get_list((111, 'acb'), None, 400)

    # value of size less than 0
    # articles/list?size=-1&page=192
    perform_get_list((-1, 192), None, 400)

    # value of page less than 0
    # articles/list?size=111&page=-99
    perform_get_list((111, -99), None, 400)

    # value of size equals to 0
    # articles/list?size=0&page=192
    perform_get_list((0, 192), None, 400)

    # value of page equals to 0
    # articles/list?size=111&page=0
    perform_get_list((111, 0), None, 400)


def test_get_content(client):

    def perform_get_content(article_id):

        url = '/articles/aid{}'.format(article_id)
        rv = client.get(url)

        print(url, rv.status_code)

        if article_id == '' or article_id == 'TEST_NOT_FOUND':
            assert 404 == rv.status_code
            if article_id == '':
                assert rv.data is None
            else:
                assert rv.data is not None
                assert json.loads(rv.data).error is not None
        else:
            assert 200 == rv.status_code
            r = {
                'id': article_id,
                'content': 'The content of article.',
                'views': 12345,
                'views_id': article_id
            }
            assert r == json.loads(rv.data)

    # 200 below
    # /article/aidT1234
    perform_get_content('T1234')
