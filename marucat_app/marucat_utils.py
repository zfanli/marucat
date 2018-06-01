#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utils module for constants and common functions"""

__author__ = 'Z.Rick'

from flask import make_response

CONTENT_TYPE = 'Content-Type'
JSON_TYPE = 'application/json'


def create_response(data, code=200):
    """创建并返回 response 对象，设置 Content-Type 声明为 JSON 类型"""
    resp = make_response(data, code)
    resp.headers[CONTENT_TYPE] = JSON_TYPE
    return resp

