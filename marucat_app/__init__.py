# -*- encoding: utf-8 -*-

from flask import Flask, make_response
from json import dumps
import articles


CONTENT_TYPE = 'Content-Type'
JSON_TYPE = 'application/json'


app = Flask('marucat_app')


@app.route('/')
def hello():
    resp = make_response(dumps({'message': 'Hello'}), 201)
    resp.headers[CONTENT_TYPE] = JSON_TYPE
    return resp


app.register_blueprint(articles.bp)

