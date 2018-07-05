#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Unit tests about articles' API"""

from logging import DEBUG

import pytest

from marucat_app import create_app


@pytest.fixture
def client():
    app = create_app(level=DEBUG, db='test')
    app.testing = True
    return app.test_client()


def test_get_list(client):
    """Test fetch list"""

    def perform_get_list(input_val, expect_val, code=200, tags=None):
        """test template

        :param input_val: inputted values (size, offset)
        :param expect_val: the expected result (size, offset)
        :param code: expected status code
        :param tags: tags
        """
        # get inputted size and offset
        size, offset = input_val if input_val else (None, None)

        # make request with query params
        # example: /articles/list?size=10&offset=1
        requested_url = '/articles{}'.format(
            '?{}{}{}'.format(
                'size={}'.format(size) if size != '' else '',
                '&' if size and offset else '',
                'offset={}'.format(offset) if offset != '' else ''
            ) if size or offset else ''
        )

        # perform request
        r = client.get(requested_url)

        print(requested_url, r.status_code)

        # check return code
        assert code == r.status_code

        if 200 == code:
            # get expected size and offset
            e_size, e_offset = expect_val
            # check Content-Type
            assert 'application/json' == r.content_type
            # check data
            fake_data = {
                'test_only': 'TESTING',
                'size': e_size,
                'offset': e_offset,
                'tags': tags
            }
            assert fake_data == r.get_json()[1]
        elif 400 == code:
            assert r.data
            assert r.get_json()['error'] is not None
        else:
            raise AssertionError(
                'Unexpected status code:{}'.format(r.status_code)
            )

    # 200 below

    # default values (size, offset)
    default_val = (10, 0)

    # default params
    perform_get_list(None, default_val)
    # specific params
    perform_get_list((55, 999), (55, 999))
    # error checking
    # no val provided to size
    perform_get_list(('', 998), (10, 998))
    # no val provided to offset
    perform_get_list((1098, ''), (1098, 0))
    # no val provided to both
    perform_get_list(('', ''), default_val)

    # 400 below

    # invalid val provided
    perform_get_list(('abc', 192), None, 400)
    perform_get_list((111, 'acb'), None, 400)
    perform_get_list((-1, 192), None, 400)
    perform_get_list((111, -99), None, 400)
    perform_get_list((0, 192), None, 400)
    perform_get_list((111, 0), None, 400)

    # other errors

    # 405 method not allowed
    rv = client.post('/articles?size=1&offset=2')
    assert 405 == rv.status_code


def test_get_content(client):
    """Test fetch content"""

    def perform_get_content(article_id, code=200):
        """Test template"""

        url = '/articles/{}'.format(article_id)
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
            r_data = r.get_json()
            assert article_id == r_data['aid']

    # 200 below
    # /article/aidT1234
    perform_get_content('T1234')

    # 404 without error message feedback below
    # /article/aid
    # perform_get_content('', 404)

    # 404 with error message feedback below
    # /article/aidTEST_NOT_FOUND
    perform_get_content('TEST_NOT_FOUND', 404)

    # special characters
    perform_get_content('/', 404)
    perform_get_content('abc/ ', 404)
    perform_get_content('abc/123', 404)
    perform_get_content('asd&123', 404)
    perform_get_content('asd+123', 404)
    perform_get_content('asd_123', 404)
    perform_get_content('asd-123', 404)
    perform_get_content('asd"123', 404)
    perform_get_content('asd\'123', 404)

    # 405 method not allowed
    rv = client.patch('/articles/aidTest')
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

        url = '/articles/{}/comments{}'.format(
            aid if aid is not None else '',
            '?{}{}{}'.format(
                'size={}'.format(size) if size is not None else '',
                '&' if size is not None and page is not None else '',
                'offset={}'.format(page) if page is not None else ''
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
            data = {
                'test_only_aid': aid,
                'size': e_size,
                'offset': e_page
            }
            assert data == r.get_json()[1]
        elif code == 400 or code == 404:
            # check Content-Type
            if aid != '' and '/' not in aid:
                assert 'application/json' == r.content_type
                assert r.get_json()['error'] is not None
            else:
                assert not r.data
        else:
            raise AssertionError(
                'Unexpected status code:{}'.format(r.status_code)
            )

    # default values
    perform_get_comments('T123', None, (10, 0))
    perform_get_comments('DF789', (99, None), (99, 0))
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
    # perform_get_comments('T123', (0, 0), None, 400)
    # perform_get_comments('T123', (0, 1), None, 400)
    # perform_get_comments('T123', (1, 0), None, 400)
    perform_get_comments('T123', (-1, -99), None, 400)
    perform_get_comments('T123', (1, -1), None, 400)
    perform_get_comments('T123', (-91, 11), None, 400)

    # method not allowed
    rv = client.put('/articles/aidT123/comments')
    assert 405 == rv.status_code


def test_post_comments(client):

    def perform_post_comments(article_id, data, code=201):

        url = '/articles/{}/comments'.format(article_id)
        r = client.post(url, json=data)

        print(url, r.status_code)

        assert code == r.status_code
        if code == 404 or code == 400:
            assert 'application/json' == r.content_type
            assert r.get_json()['error'] is not None

    normally_data = {
        'from': 'Richard',
        'body': 'Ok!',
        'timestamp': 1529658047.974455
    }

    # normally
    perform_post_comments('1234', normally_data)
    # invalid article ID
    perform_post_comments('123$123', normally_data, 404)
    perform_post_comments('123"123', normally_data, 404)
    perform_post_comments('123+123', normally_data, 404)
    perform_post_comments('123-123', normally_data, 404)
    perform_post_comments("123'123", normally_data, 404)
    # invalid post data
    perform_post_comments('test1234', {'from': 'a', 'body': 'b'}, 400)
    perform_post_comments('test1234', {'timestamp': 'a', 'body': 'b'}, 400)
    perform_post_comments('test1234', {'timestamp': 'a', 'from': 'b'}, 400)
    # reply to ok
    perform_post_comments('asd123123', {**normally_data, 'reply_to': '12412'})


def test_delete_comment(client):

    def perform_delete_comment(article_id, comment_id, code=200):

        url = '/articles/{}/comments/{}'.format(
            article_id, comment_id
        )

        r = client.delete(url)

        print(url, r.status_code)

        assert code == r.status_code
        if code == 404:
            assert 'application/json' == r.content_type
            assert r.get_json()['error'] is not None

    # normally
    perform_delete_comment('aid1234', 'cid1234')
    # bad article ID
    perform_delete_comment('aid+123', 'cid456', 404)
    perform_delete_comment('aid-123', 'cid456', 404)
    perform_delete_comment('aid*123', 'cid456', 404)
    perform_delete_comment(r'aid\123', 'cid456', 404)
    perform_delete_comment('aid"123', 'cid456', 404)
    perform_delete_comment('aid123%', 'cid456', 404)
    # perform_delete_comment('aid#123', 'cid456', 404)
    # perform_delete_comment('aid123#', 'cid456', 404)
    perform_delete_comment('aid@123', 'cid456', 404)
    perform_delete_comment('aid&123', 'cid456', 404)
    perform_delete_comment("aid'123", 'cid456', 404)
    # bad comment ID
    perform_delete_comment('aid1234', 'cid~123', 404)
    perform_delete_comment('aid1234', 'cid!123', 404)
    perform_delete_comment('aid1234', 'cid@123', 404)
    perform_delete_comment('aid1234', 'cid$123', 404)
    perform_delete_comment('aid1234', 'cid123%', 404)
    perform_delete_comment('aid1234', 'cid^123', 404)
    perform_delete_comment('aid1234', 'cid&123', 404)
    perform_delete_comment('aid1234', 'cid*123', 404)
    perform_delete_comment('aid1234', 'cid(123', 404)
    perform_delete_comment('aid1234', 'cid)123', 404)
    perform_delete_comment('aid1234', 'cid[123', 404)
    perform_delete_comment('aid1234', 'cid]123', 404)
