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
Tempest service class for service test cases
"""

import json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class ServiceClient(base.BaseContrailClient):

    """
    Service class for service client test cases
    """

    def list_service_templates(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/service-templates'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_service_templates(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/service-templates'
        post_body = json.dumps({'service-template': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_service_template(self, template_id):
        """
        :param template_id:
        :return:
        """
        url = '/service-template/%s' % str(template_id)
        return self.get(url)

    def delete_service_template(self, template_id):
        """
        :param template_id:
        :return:
        """
        url = '/service-template/%s' % str(template_id)
        return self.delete(url)

    def update_service_template(self, template_id, **kwargs):
        """
        :param template_id:
        :param kwargs:
        :return:
        """
        url = '/service-template/%s' % str(template_id)
        put_data = {'service-template': kwargs}
        req_put_data = json.dumps(put_data)
        resp, body = self.put(url, req_put_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def list_service_health_checks(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/service-health-checks'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_service_health_checks(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/service-health-checks'
        post_body = json.dumps({'service-health-check': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_service_health_check(self, template_id):
        """
        :param template_id:
        :return:
        """
        url = '/service-health-check/%s' % str(template_id)
        return self.get(url)

    def delete_service_health_check(self, template_id):
        """
        :param template_id:
        :return:
        """
        url = '/service-health-check/%s' % str(template_id)
        return self.delete(url)

    def update_service_health_check(self, template_id, **kwargs):
        """
        :param template_id:
        :param kwargs:
        :return:
        """
        url = '/service-health-check/%s' % str(template_id)
        put_data = {'service-health-check': kwargs}
        req_put_data = json.dumps(put_data)
        resp, body = self.put(url, req_put_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_service_instances(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/service-instances'
        post_body = json.dumps({'service-instance': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_service_instance(self, template_id):
        """
        :param template_id:
        :return:
        """
        url = '/service-instance/%s' % str(template_id)
        return self.get(url)

    def delete_service_instance(self, template_id):
        """
        :param template_id:
        :return:
        """
        url = '/service-instance/%s' % str(template_id)
        return self.delete(url)

    def list_service_instances(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/service-instances'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def update_service_instance(self, template_id, **kwargs):
        """
        :param template_id:
        :param kwargs:
        :return:
        """
        url = '/service-instance/%s' % str(template_id)
        put_data = {'service-instance': kwargs}
        req_put_data = json.dumps(put_data)
        resp, body = self.put(url, req_put_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
