#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Integrate the app, register blueprints and handle errors"""

from flask import Flask
from werkzeug.exceptions import MethodNotAllowed, NotFound
from json import dumps
from logging import basicConfig, DEBUG
from marucat_app.marucat_utils import create_response
import marucat_app.articles as articles

# logging configuration
basicConfig(
    level=DEBUG,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
# create flask instance with package name
app = Flask('marucat_app')


@app.route('/')
def hello():
    """A greeting when the root path was visited"""
    resp = create_response(dumps({'message': 'Hello'}), 200)
    return resp


@app.errorhandler(MethodNotAllowed)
def method_not_allowed(e):
    """When method is not allowed return nothing but state code only"""
    app.logger.warn(e)
    return '', 405


@app.errorhandler(NotFound)
def not_found(e):
    """Whet the requested URL is not exist return state code only"""
    app.logger.warn(e)
    return '', 404


# register all APIs about articles
app.register_blueprint(articles.bp)
