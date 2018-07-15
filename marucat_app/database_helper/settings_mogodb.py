#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Settings connector, driven by MongoDb."""


class SettingsConnector(object):

    def __init__(self, collection):
        """Initial connector

        :param collection: collection
        """
        self._collection = collection

    def get_list(self):
        pass

    def get_one(self, name):
        pass

    def update_one(self, name, data):
        pass

    def delete_one(self, name):
        pass
