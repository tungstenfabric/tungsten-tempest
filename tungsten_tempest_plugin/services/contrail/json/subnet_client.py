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
Tempest service class for subnet test cases
"""

import json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class SubnetClient(base.BaseContrailClient):

    """
    Service class for subnet client test cases
    """

    def list_subnets(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/subnets'
        if params:
            url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_subnets(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/subnets'
        resp, body = self.post(url, json.dumps({'subnet': kwargs}))
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_subnet(self, uuid, params=None):
        """
        :param uuid:
        :param params:
        :return:
        """
        url = '/subnet/{0}'.format(uuid)
        if params:
            url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_subnet(self, uuid, **kwargs):
        """
        :param uuid:
        :param kwargs:
        :return:
        """
        url = '/subnet/{0}'.format(uuid)
        resp, body = self.put(url, json.dumps({'subnet': kwargs}))
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_subnet(self, uuid):
        """
        :param uuid:
        :return:
        """
        url = '/subnet/{0}'.format(uuid)
        return self.delete(url)
