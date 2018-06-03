#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Integrate the app, register blueprints and handle errors"""

from flask import Flask, jsonify
from logging import basicConfig, ERROR
from marucat_app.articles import bp as articles


# create flask application
def create_app(*, level=ERROR):

    # logging configuration
    basicConfig(
        level=level,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    app = Flask('marucat_app')

    @app.route('/')
    def hello():
        """A greeting when the root path was visited"""
        return jsonify({'message': 'Hello'}), 202

    @app.errorhandler(404)
    @app.errorhandler(405)
    def method_not_allowed(e):
        """Handler for NotFound and MethodNotAllowed"""
        app.logger.warning('Error happened: {}'.format(e.name))
        return '', e.code

    # register blueprints
    app.register_blueprint(articles)

    return app
