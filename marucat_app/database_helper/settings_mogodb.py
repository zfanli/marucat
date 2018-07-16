#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Settings connector, driven by MongoDb."""
from pymongo import ReturnDocument

from marucat_app.utils.utils import deal_with_object_id


class SettingsConnector(object):

    def __init__(self, collection):
        """Initial connector

        :param collection: collection
        """
        self._collection = collection

    def get_list(self, *, size, offset):
        """Get settings list

        :param size: paging size
        :param offset: skip
        :return: list of settings
        """
        li = self._collection.find({}).skip(offset).limit(size)
        return deal_with_object_id(li)

    def get_one(self, name):
        """Get specified one of settings

        :param name: name
        :return: specified one
        """
        result = self._collection.find_one({'name': name})
        return deal_with_object_id(result)

    def update_one(self, name, data):
        """Update settings

        :param name: name
        :param data: data
        :return: updated object
        """
        # TODO deal with data
        result = self._collection.find_one_and_update({'name': name}, data, return_document=ReturnDocument.AFTER)
        return deal_with_object_id(result)

    def delete_one(self, name):
        """Delete specified one of settings

        :param name: name
        :return: True or False tell you
        """
        result = self._collection.delete_one({'name': name})
        return bool(result.deleted_count)
