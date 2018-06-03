#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""App runner"""

from logging import DEBUG
from marucat_app import create_app

app = create_app(level=DEBUG)
app.run(debug=True)
