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
Tempest service class for alarm ip client test cases
"""

import json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class AliasIPsClient(base.BaseContrailClient):

    """
    Service class for alias ip test cases
    """

    def list_alias_ip_pools(self, params=None):
        """
        :param params:
        :return: response object
        """
        url = '/alias-ip-pools'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_alias_ip_pools(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/alias-ip-pools'
        post_body = json.dumps({'alias-ip-pool': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_alias_ip_pool(self, pool_id):
        """
        :param pool_id:
        :return: response object
        """
        url = '/alias-ip-pool/%s' % str(pool_id)
        return self.get(url)

    def delete_alias_ip_pool(self, pool_id):
        """
        :param pool_id:
        :return: response object
        """
        url = '/alias-ip-pool/%s' % str(pool_id)
        return self.delete(url)

    def update_alias_ip_pool(self, pool_id, **kwargs):
        """
        :param pool_id:
        :param kwargs:
        :return: map object
        """
        url = '/alias-ip-pool/%s' % str(pool_id)
        post_data = {'alias-ip-pool': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(url, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def list_alias_ips(self, params=None):
        """
        :param params:
        :return: response object
        """
        url = '/alias-ips'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_alias_ips(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/alias-ips'
        post_body = json.dumps({'alias-ip': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_alias_ip(self, ip_id):
        """
        :param ip_id:
        :return: response object
        """
        url = '/alias-ip/%s' % str(ip_id)
        return self.get(url)

    def delete_alias_ip(self, ip_id):
        """
        :param ip_id:
        :return: response object
        """
        url = '/alias-ip/%s' % str(ip_id)
        return self.delete(url)

    def update_alias_ip(self, ip_id, **kwargs):
        """
        :param ip_id:
        :param kwargs:
        :return: map object
        """
        url = '/alias-ip/%s' % str(ip_id)
        post_data = {'alias-ip': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(url, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
