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
Tempest service class for dns test cases
"""

import json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


# noinspection PyPep8Naming
class VirtualDNSClient(base.BaseContrailClient):

    """
    Service class for virtual dns test cases
    """

    def list_virtual_dns(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/virtual-DNSs'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_virtual_dns(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/virtual-DNSs'
        post_body = json.dumps({'virtual-DNS': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_virtual_dns(self, dns_id):
        """
        :param dns_id:
        :return:
        """
        url = '/virtual-DNS/%s' % dns_id
        return self.get(url)

    def delete_virtual_dns(self, dns_id):
        """
        :param dns_id:
        :return:
        """
        url = '/virtual-DNS/%s' % dns_id
        return self.delete(url)

    def update_virtual_dns(self, dns_id, **kwargs):
        """
        :param dns_id:
        :param kwargs:
        :return:
        """
        url = '/virtual-DNS/%s' % dns_id
        post_body = json.dumps({'virtual-DNS': kwargs})
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def list_virtual_dns_records(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/virtual-DNS-records'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_virtual_dns_records(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/virtual-DNS-records'
        post_body = json.dumps({'virtual-DNS-record': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_virtual_dns_record(self, dns_record_id):
        """
        :param dns_record_id:
        :return:
        """
        url = 'virtual-DNS-record/%s' % dns_record_id
        return self.delete(url)

    def show_virtual_dns_record(self, dns_record_id):
        """
        :param dns_record_id:
        :return:
        """
        url = '/virtual-DNS-record/%s' % dns_record_id
        return self.get(url)

    def update_virtual_dns_record(self, dns_record_id, **kwargs):
        """
        :param dns_record_id:
        :param kwargs:
        :return:
        """
        url = '/virtual-DNS-record/%s' % dns_record_id
        post_body = json.dumps({'virtual-DNS-record': kwargs})
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
