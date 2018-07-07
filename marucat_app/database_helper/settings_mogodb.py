#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Settings connector, driven by MongoDb."""


class SettingsConnector(object):

    def __init__(self, collection):
        """Initial connector

        :param collection: collection
        """
        self._collection = collection
