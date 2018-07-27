# Copyright 2016 AT&T Corp
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Tempest service class for database test cases
"""

from oslo_serialization import jsonutils as json
from tungsten_tempest_plugin.services.contrail.json import base


class ContrailDatabaseClient(base.BaseContrailClient):

    """
    Service class for database test cases
    """

    def list_database_nodes(self):
        """
        :return: response object
        """
        url = '/database-nodes'
        return self.get(url)

    def show_database_node(self, db_node_id):
        """
        :param db_node_id:
        :return: response object
        """
        url = '/database-node/%s' % db_node_id
        return self.get(url)

    def create_databse_nodes(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        post_body = json.dumps({'database-node': kwargs})
        url = '/database-nodes'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_database_node(self, db_node_id):
        """
        :param db_node_id:
        :return: response object
        """
        url = '/database-node/%s' % db_node_id
        return self.delete(url)

    def update_database_node(self, db_node_id, **kwargs):
        """
        :param db_node_id:
        :param kwargs:
        :return: map object
        """
        post_body = json.dumps({'database-node': kwargs})
        url = '/database-node/%s' % db_node_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
