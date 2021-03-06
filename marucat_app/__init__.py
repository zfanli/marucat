#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Integrate the app, register blueprints and handle errors"""

from logging import basicConfig, ERROR

from flask import Flask, jsonify

from marucat_app.database_helper import ConnectorCreator
from marucat_app.articles import bp as articles
from marucat_app.settings import bp as settings
from marucat_app.utils.utils import (
    CONNECTOR_FACTORY, APP_NAME
)
from marucat_app.utils.messages import create_error_message


# create flask application
def create_app(*, level=ERROR, db='mongodb', test_flag=False):

    # logging configuration
    basicConfig(
        level=level,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    app = Flask(APP_NAME)

    app.config[CONNECTOR_FACTORY] = ConnectorCreator(db, test=test_flag)
    app.url_map.strict_slashes = False

    @app.route('/')
    def _hello():
        """A greeting when the root path was visited"""
        return jsonify({'message': 'Hello'}), 202

    @app.errorhandler(404)
    @app.errorhandler(405)
    def _not_found_or_method_not_allowed(e):
        """Handler for NotFound and MethodNotAllowed"""
        app.logger.warning('Error happened: {}'.format(e.name))
        return '', e.code

    @app.errorhandler(500)
    def _server_error(e):
        """Handler for server errors"""
        app.logger.error('Error happened: {}'.format(e.name))
        return jsonify(create_error_message(e.description)), 500

    # register blueprints
    app.register_blueprint(articles)
    app.register_blueprint(settings)

    return app
