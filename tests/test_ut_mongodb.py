#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Description here"""
from marucat_app.database_helper import ConnectorCreator


def test_connection():

    c = ConnectorCreator('mongodb')

