#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Integration"""

__author__ = 'Z.Rick'

from flask import Flask, make_response
from json import dumps
from marucat_app.marucat_utils import CONTENT_TYPE, JSON_TYPE
import marucat_app.articles as articles


app = Flask('marucat_app')

with app.app_context() as ctx:
    ctx.pop(app.logger)


@app.route('/')
def hello():
    resp = make_response(dumps({'message': 'Hello'}), 200)
    resp.headers[CONTENT_TYPE] = JSON_TYPE
    return resp


app.register_blueprint(articles.bp)
