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
Tempest service class for access control test cases
"""

import json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class AccessControlClient(base.BaseContrailClient):

    """
    Service class for access control test cases
    """

    def list_access_control_lists(self, params=None):
        """
        :param params:
        :return: list object
        """
        url = '/access-control-lists'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_access_control_lists(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/access-control-lists'
        post_body = json.dumps({'access-control-list': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_access_control_list(self, list_id):
        """
        :param list_id:
        :return: response object
        """
        url = '/access-control-list/%s' % str(list_id)
        return self.get(url)

    def delete_access_control_list(self, list_id):
        """
        :param list_id:
        :return: response object
        """
        url = '/access-control-list/%s' % str(list_id)
        return self.delete(url)

    def update_access_control_list(self, list_id, **kwargs):
        """
        :param list_id:
        :param kwargs:
        :return: map object
        """
        url = '/access-control-list/%s' % str(list_id)
        post_data = {'access-control-list': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(url, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def list_api_access_lists(self, params=None):
        """
        :param params:
        :return: response object
        """
        url = '/api-access-lists'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_api_access_lists(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/api-access-lists'
        post_body = json.dumps({'api-access-list': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_api_access_list(self, list_id):
        """
        :param list_id:
        :return: response object
        """
        url = '/api-access-list/%s' % str(list_id)
        return self.get(url)

    def delete_api_access_list(self, list_id):
        """
        :param list_id:
        :return: response object
        """
        url = '/api-access-list/%s' % str(list_id)
        return self.delete(url)

    def update_api_access_list(self, list_id, **kwargs):
        """
        :param list_id:
        :param kwargs:
        :return: map object
        """
        url = '/api-access-list/%s' % str(list_id)
        post_data = {'api-access-list': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(url, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
