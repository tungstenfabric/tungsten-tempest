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
Tempest service class for attachment clients test cases
"""

import json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class AttachmentsClient(base.BaseContrailClient):

    """
    Service class for attachment client test cases
    """

    def list_provider_attachments(self, params=None):
        """
        :param params:
        :return: response object
        """
        url = '/provider-attachments'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_provider_attachments(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/provider-attachments'
        post_body = json.dumps({'provider-attachment': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_provider_attachment(self, appliance_id):
        """
        :param appliance_id:
        :return: response object
        """
        url = '/provider-attachment/%s' % str(appliance_id)
        return self.get(url)

    def delete_provider_attachment(self, appliance_id):
        """
        :param appliance_id:
        :return: response object
        """
        url = '/provider-attachment/%s' % str(appliance_id)
        return self.delete(url)

    def update_provider_attachment(self, appliance_id, **kwargs):
        """
        :param appliance_id:
        :param kwargs:
        :return: map object
        """
        url = '/provider-attachment/%s' % str(appliance_id)
        post_data = {'provider-attachment': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(url, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def list_customer_attachments(self, params=None):
        """
        :param params:
        :return: response object
        """
        url = '/customer-attachments'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_customer_attachments(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/customer-attachments'
        post_body = json.dumps({'customer-attachment': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_customer_attachment(self, appliance_id):
        """
        :param appliance_id:
        :return: response object
        """
        url = '/customer-attachment/%s' % str(appliance_id)
        return self.get(url)

    def delete_customer_attachment(self, appliance_id):
        """
        :param appliance_id:
        :return: response object
        """
        url = '/customer-attachment/%s' % str(appliance_id)
        return self.delete(url)

    def update_customer_attachment(self, appliance_id, **kwargs):
        """
        :param appliance_id:
        :param kwargs:
        :return: map object
        """
        url = '/customer-attachment/%s' % str(appliance_id)
        post_data = {'customer-attachment': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(url, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
