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
Tempest service class for interface test cases
"""

from oslo_serialization import jsonutils as json
from tungsten_tempest_plugin.services.contrail.json import base


class InterfaceClient(base.BaseContrailClient):

    """
    Service class for interface test cases
    """

    def list_physical_interfaces(self):
        """
        :return: response object
        """
        url = '/physical-interfaces'
        return self.get(url)

    def create_physical_interfaces(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/physical-interfaces'
        post_body = json.dumps({'physical-interface': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_physical_interface(self, uuid, **kwargs):
        """
        :param uuid:
        :param kwargs:
        :return: map object
        """
        url = '/physical-interface/%s' % uuid
        post_data = {'physical-interface': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(url, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_physical_interface(self, uuid):
        """
        :param uuid:
        :return: response object
        """
        url = '/physical-interface/%s' % uuid
        return self.delete(url)

    def show_physical_interface(self, uuid):
        """
        :param uuid:
        :return: map object
        """
        url = '/physical-interface/%s' % uuid
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def list_logical_interfaces(self):
        """
        :return: response object
        """
        url = '/logical-interfaces'
        return self.get(url)

    def create_logical_interfaces(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/logical-interfaces'
        post_body = json.dumps({'logical-interface': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_logical_interface(self, uuid, **kwargs):
        """
        :param uuid:
        :param kwargs:
        :return: map object
        """
        url = '/logical-interface/%s' % uuid
        post_data = {'logical-interface': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(url, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_logical_interface(self, uuid):
        """
        :param uuid:
        :return: response object
        """
        url = '/logical-interface/%s' % uuid
        return self.delete(url)

    def show_logical_interface(self, uuid):
        """
        :param uuid:
        :return: map object
        """
        url = '/logical-interface/%s' % uuid
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
