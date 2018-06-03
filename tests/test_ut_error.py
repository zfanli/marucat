#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Unit tests about error handlers"""

import pytest
from logging import DEBUG
from marucat_app import create_app


@pytest.fixture
def client():
    app = create_app(level=DEBUG)
    app.testing = True
    return app.test_client()


def test_hello(client):
    """testing the greeting message"""
    rv = client.get('/')
    assert 202 == rv.status_code
    assert b'{"message":"Hello"}' in rv.data


def test_not_found(client):
    """testing the 404 handler"""
    rv = client.get('/some-path-did-not-exists')
    assert 404 == rv.status_code
    assert b'' == rv.data


def test_method_not_allowed(client):
    """testing the 405 handler"""
    rv = client.post('/')
    assert 405 == rv.status_code
    assert b'' == rv.data
