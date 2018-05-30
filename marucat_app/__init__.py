# -*- encoding: utf-8 -*-

from flask import Flask, make_response
import json

app = Flask(__name__)


@app.route('/')
def hello():
    resp = make_response(json.dumps({'message': 'Hello'}), 201)
    resp.headers['Content-Type'] = 'application/json'
    return resp

