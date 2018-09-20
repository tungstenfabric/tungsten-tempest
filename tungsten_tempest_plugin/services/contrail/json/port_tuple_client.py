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
Tempest service class for tuple test cases
"""

import json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class PortTupleClient(base.BaseContrailClient):


    def list_port_tuples(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/port-tuples'
        if params:
            url += '?{0}'.format(urllib.urlencode(params))
        return self.get(url)

    def show_port_tuple(self, uuid):
        """
        :param uuid:
        :return:
        """
        url = '/port-tuple/{0}'.format(uuid)
        return self.get(url)

    def create_port_tuples(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/port-tuples'
        post_body = json.dumps({'port-tuple': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_port_tuple(self, uuid, **kwargs):
        """
        :param uuid:
        :param kwargs:
        :return:
        """
        url = '/port-tuple/{0}'.format(uuid)
        put_body = json.dumps({'port-tuple': kwargs})
        resp, body = self.put(url, put_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_port_tuple(self, uuid):
        """
        :param uuid:
        :return:
        """
        url = '/port-tuple/{0}'.format(uuid)
        return self.delete(url)
