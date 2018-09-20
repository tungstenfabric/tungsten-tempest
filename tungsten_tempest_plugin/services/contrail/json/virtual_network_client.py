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
Tempest service class for virtual network test cases
"""

from oslo_serialization import jsonutils as json
from tungsten_tempest_plugin.services.contrail.json import base


class VirtualNetworkClient(base.BaseContrailClient):

    """
    Service class for virtual n/w test cases
    """

    def list_virtual_networks(self):
        """
        :return:
        """
        url = '/virtual-networks'
        return self.get(url)

    def create_virtual_networks(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/virtual-networks'
        post_body = json.dumps({'virtual-network': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_virtual_network(self, uuid, **kwargs):
        """
        :param uuid:
        :param kwargs:
        :return:
        """
        url = '/virtual-network/%s' % uuid
        post_data = {'virtual-network': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(url, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_virtual_network(self, uuid):
        """
        :param uuid:
        :return:
        """
        url = '/virtual-network/%s' % uuid
        return self.delete(url)

    def show_virtual_network(self, uuid):
        """
        :param uuid:
        :return:
        """
        url = '/virtual-network/%s' % uuid
        return self.get(url)
