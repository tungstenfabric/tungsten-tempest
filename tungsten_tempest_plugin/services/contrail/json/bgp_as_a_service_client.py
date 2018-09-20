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
Tempest service class for BGP as a service test cases
"""

import json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class BGPAsAServiceClient(base.BaseContrailClient):

    """
    Service class for bgp as a service test cases
    """

    def list_bgp_as_a_services(self, params=None):
        """
        :param params:
        :return: response object
        """
        url = '/bgp-as-a-services'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_bgp_as_a_services(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/bgp-as-a-services'
        post_body = json.dumps({'bgp-as-a-service': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_bgp_as_a_service(self, bgp_id):
        """
        :param bgp_id:
        :return: response object
        """
        url = '/bgp-as-a-service/%s' % str(bgp_id)
        return self.get(url)

    def delete_bgp_as_a_service(self, bgp_id):
        """
        :param bgp_id:
        :return: response object
        """
        url = '/bgp-as-a-service/%s' % str(bgp_id)
        return self.delete(url)

    def update_bgp_as_a_service(self, bgp_id, **kwargs):
        """
        :param bgp_id:
        :param kwargs:
        :return: map object
        """
        url = '/bgp-as-a-service/%s' % str(bgp_id)
        post_data = {'bgp-as-a-service': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(url, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
