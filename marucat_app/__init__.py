#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Integrate the app, register blueprints and handle errors"""

from flask import Flask, jsonify
from logging import basicConfig, ERROR
from marucat_app.db_connector import ConnectorCreator
from marucat_app.articles import bp as articles
from marucat_app.marucat_utils import (
    create_error_message, CONNECTOR_FACTORY, APP_NAME
)


# create flask application
def create_app(*, level=ERROR, db='mongodb'):

    # logging configuration
    basicConfig(
        level=level,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    app = Flask(APP_NAME)

    app.config[CONNECTOR_FACTORY] = ConnectorCreator(db)

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

    return app
