# -*- encoding: utf-8 -*-

from flask import Blueprint


bp = Blueprint('articles', __name__)


@bp.route('/test')
def articles_test():
    return 'test'

