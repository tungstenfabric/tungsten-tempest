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
Tempest service class for dsa rule test cases
"""

import json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class DSARuleClient(base.BaseContrailClient):

    """
    Service class for dsa rules test cases
    """

    def list_dsa_rules(self, params=None):
        """
        :param params:
        :return: response object
        """
        url = '/dsa-rules'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_dsa_rules(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/dsa-rules'
        post_body = json.dumps({'dsa-rule': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_dsa_rule(self, dns_id):
        """
        :param dns_id:
        :return: response object
        """
        url = '/dsa-rule/%s' % dns_id
        return self.get(url)

    def delete_dsa_rule(self, dns_id):
        """
        :param dns_id:
        :return: response object
        """
        url = '/dsa-rule/%s' % dns_id
        return self.delete(url)

    def update_dsa_rule(self, dns_id, **kwargs):
        """
        :param dns_id:
        :param kwargs:
        :return: map object
        """
        url = '/dsa-rule/%s' % dns_id
        post_body = json.dumps({'dsa-rule': kwargs})
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
