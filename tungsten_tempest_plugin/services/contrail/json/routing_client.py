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
Tempest service class for routing test cases
"""

import json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class RoutingClient(base.BaseContrailClient):

    """
    Service class for routing test cases
    """

    def list_routing_instances(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/routing-instances'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_routing_instances(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/routing-instances'
        post_body = json.dumps({'routing-instance': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_routing_instance(self, instance_id):
        """

        :param instance_id:
        :return:
        """
        url = '/routing-instance/%s' % str(instance_id)
        return self.get(url)

    def delete_routing_instance(self, instance_id):
        """

        :param instance_id:
        :return:
        """
        url = '/routing-instance/%s' % str(instance_id)
        return self.delete(url)

    def update_routing_instance(self, instance_id, **kwargs):
        """

        :param instance_id:
        :param kwargs:
        :return:
        """
        url = '/routing-instance/%s' % str(instance_id)
        post_data = {'routing-instance': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(url, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
