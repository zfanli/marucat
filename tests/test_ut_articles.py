#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Unit tests about API of articles"""

import pytest
from logging import DEBUG
from marucat_app import create_app


@pytest.fixture
def client():
    app = create_app(level=DEBUG, db='test')
    app.testing = True
    return app.test_client()


def test_get_list(client):
    """Test fetch list"""

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
        r = client.get(requested_url)

        print(requested_url, r.status_code)

        # check return code
        assert code == r.status_code

        if 200 == code:
            # get expected size and page
            e_size, e_page = expect_val
            # check Content-Type
            assert 'application/json' == r.content_type
            # check data
            assert [{'id': 1, 'size': e_size}, {'id': 2, 'page': e_page}] == r.get_json()
        elif 400 == code:
            assert r.data
            assert r.get_json()['error'] is not None
        else:
            raise AssertionError('Unexpected status code:{}'.format(r.status_code))

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

    # invalid val provided
    # articles/list?size=abc&page=192
    perform_get_list(('abc', 192), None, 400)
    # articles/list?size=111&page=acb
    perform_get_list((111, 'acb'), None, 400)
    # articles/list?size=-1&page=192
    perform_get_list((-1, 192), None, 400)
    # articles/list?size=111&page=-99
    perform_get_list((111, -99), None, 400)
    # articles/list?size=0&page=192
    perform_get_list((0, 192), None, 400)
    # articles/list?size=111&page=0
    perform_get_list((111, 0), None, 400)

    # other errors

    # 405 method not allowed
    rv = client.post('/articles/list?size=1&page=2')
    assert 405 == rv.status_code


def test_get_content(client):
    """Test fetch content"""

    def perform_get_content(article_id, code=200):
        """Test template"""

        url = '/articles/aid{}'.format(article_id)
        r = client.get(url)

        print(url, r.status_code)

        assert code == r.status_code

        if 404 == code:
            if article_id == '' or '/' in article_id:
                assert not r.data
            else:
                assert r.data
                assert r.get_json()['error'] is not None
        else:
            er = {
                'id': article_id,
                'content': 'The content of article.',
                'views': 12345,
                'views_id': article_id
            }
            assert er == r.get_json()

    # 200 below
    # /article/aidT1234
    perform_get_content('T1234')

    # 404 without error message feedback below
    # /article/aid
    perform_get_content('', 404)

    # 404 with error message feedback below
    # /article/aidTEST_NOT_FOUND
    perform_get_content('TEST_NOT_FOUND', 404)

    # special characters
    perform_get_content('/', 404)
    perform_get_content('abc/', 404)
    perform_get_content('abc/123', 404)
    perform_get_content('asd&123', 404)
    perform_get_content('asd+123', 404)
    perform_get_content('asd_123', 404)
    perform_get_content('asd-123', 404)
    perform_get_content('asd"123', 404)
    perform_get_content('asd\'123', 404)

    # 405 method not allowed
    rv = client.post('/articles/aidTest')
    assert 405 == rv.status_code


def test_get_comments(client):
    """Test fetch comments"""

    def perform_get_comments(aid, inputted, expect, code=200):
        """Test template

        :param aid: article id
        :param inputted: inputted values
        :param expect: expected result
        :param code: status code
        """

        size, page = None, None
        if inputted is not None:
            size, page = inputted

        url = '/articles/aid{}/comments{}'.format(
            aid if aid is not None else '',
            '?{}{}{}'.format(
                'size={}'.format(size) if size is not None else '',
                '&' if size is not None and page is not None else '',
                'page={}'.format(page) if page is not None else ''
            ) if size is not None or page is not None else ''
        )

        r = client.get(url)

        print(url, r.status_code)

        assert code == r.status_code

        if code == 200:
            # get expected size and page
            e_size, e_page = expect
            # check Content-Type
            assert 'application/json' == r.content_type
            # check data
            data = {'id': aid, 'comments': 'Test comments', 'size': e_size, 'page': e_page}
            assert data == r.get_json()
        elif code == 400 or code == 404:
            # check Content-Type
            if aid != '' and '/' not in aid:
                assert 'application/json' == r.content_type
                assert r.get_json()['error'] is not None
            else:
                assert not r.data
        else:
            raise AssertionError('Unexpected status code:{}'.format(r.status_code))

    # default values
    perform_get_comments('T123', None, (10, 1))
    perform_get_comments('DF789', (99, None), (99, 1))
    perform_get_comments('090909', (None, 12), (10, 12))

    # normally test
    perform_get_comments('paa', (123, 456), (123, 456))
    perform_get_comments('0998100029999123', (11, 12), (11, 12))

    # bad parameters
    perform_get_comments('', None, None, 404)
    perform_get_comments('/', None, None, 404)
    perform_get_comments('asd/123', (1, 2), None, 404)
    perform_get_comments('asd&123', (3, 4), None, 404)
    perform_get_comments('asd+123', None, None, 404)
    perform_get_comments('asd-123', None, None, 404)
    perform_get_comments('asd_123', (5, 6), None, 404)
    perform_get_comments('asd\'123', (7, 8), None, 404)
    perform_get_comments('asd"123', None, None, 404)

    # bad query parameters
    perform_get_comments('T123', (0, 0), None, 400)
    perform_get_comments('T123', (0, 1), None, 400)
    perform_get_comments('T123', (1, 0), None, 400)
    perform_get_comments('T123', (-1, -99), None, 400)
    perform_get_comments('T123', (1, -1), None, 400)
    perform_get_comments('T123', (-91, 11), None, 400)

    # method not allowed
    rv = client.put('/articles/aidT123/comment')
    assert 404 == rv.status_code
