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
Tempest service class for service appliance test cases
"""

import json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class ServiceAppliancesClient(base.BaseContrailClient):

    """
    Service class for service appliances test cases
    """

    def list_service_appliances(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/service-appliances'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_service_appliances(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/service-appliances'
        post_body = json.dumps({'service-appliance': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_service_appliance(self, appliance_id):
        """
        :param appliance_id:
        :return:
        """
        url = '/service-appliance/%s' % str(appliance_id)
        return self.get(url)

    def delete_service_appliance(self, appliance_id):
        """
        :param appliance_id:
        :return:
        """
        url = '/service-appliance/%s' % str(appliance_id)
        return self.delete(url)

    def update_service_appliance(self, appliance_id, **kwargs):
        """
        :param appliance_id:
        :param kwargs:
        :return:
        """
        url = '/service-appliance/%s' % str(appliance_id)
        post_data = {'service-appliance': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(url, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def list_service_appliance_sets(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/service-appliance-sets'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_service_appliance_sets(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/service-appliance-sets'
        post_body = json.dumps({'service-appliance-set': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_service_appliance_set(self, appliance_id):
        """
        :param appliance_id:
        :return:
        """
        url = '/service-appliance-set/%s' % str(appliance_id)
        return self.get(url)

    def delete_service_appliance_set(self, appliance_id):
        """
        :param appliance_id:
        :return:
        """
        url = '/service-appliance-set/%s' % str(appliance_id)
        return self.delete(url)

    def update_service_appliance_set(self, appliance_id, **kwargs):
        """
        :param appliance_id:
        :param kwargs:
        :return:
        """
        url = '/service-appliance-set/%s' % str(appliance_id)
        post_data = {'service-appliance-set': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(url, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
