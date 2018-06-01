#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Integration"""

from flask import Flask, make_response
from json import dumps
from logging import basicConfig, DEBUG
from marucat_app.marucat_utils import CONTENT_TYPE, JSON_TYPE
import marucat_app.articles as articles

# logging configuration
basicConfig(
    level=DEBUG,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
# create flask instance with package name
app = Flask('marucat_app')


# greeting message
@app.route('/')
def hello():
    resp = make_response(dumps({'message': 'Hello'}), 200)
    resp.headers[CONTENT_TYPE] = JSON_TYPE
    return resp


# register all APIs about articles
app.register_blueprint(articles.bp)
