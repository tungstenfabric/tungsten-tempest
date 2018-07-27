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
Tempest service class for analytics node test cases
"""

import json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class AnalyticsNodeClient(base.BaseContrailClient):

    """
    Service class for analytics node test cases
    """

    def list_analytics_nodes(self, params=None):
        """
        :param params:
        :return: response object
        """
        url = '/analytics-nodes'
        if params:
            url += '?{0}'.format(urllib.urlencode(params))
        return self.get(url)

    def show_analytics_node(self, uuid):
        """
        :param uuid:
        :return: response object
        """
        url = '/analytics-node/{0}'.format(uuid)
        return self.get(url)

    def create_analytics_nodes(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/analytics-nodes'
        post_body = json.dumps({'analytics-node': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_analytics_node(self, uuid, **kwargs):
        """
        :param uuid:
        :param kwargs:
        :return: map object
        """
        url = '/analytics-node/{0}'.format(uuid)
        put_body = json.dumps({'analytics-node': kwargs})
        resp, body = self.put(url, put_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_analytics_node(self, uuid):
        """
        :param uuid:
        :return: response object
        """
        url = '/analytics-node/{0}'.format(uuid)
        return self.delete(url)
