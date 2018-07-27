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
Tempest service class for instance IP test cases
"""

from oslo_serialization import jsonutils as json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class InstanceIPClient(base.BaseContrailClient):

    """
    Service class for instance ip test cases
    """

    def list_instance_ips(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/instance-ips'
        if kwargs:
            url += '?%s' % urllib.urlencode(kwargs)
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_instance_ips(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/instance-ips'
        post_body = {'instance-ip': kwargs}
        resp, body = self.post(url, json.dumps(post_body))
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_instance_ip(self, uuid):
        """
        :param uuid:
        :return: map object
        """
        url = '/instance-ip/{0}'.format(uuid)
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_instance_ip(self, uuid, **kwargs):
        """
        :param uuid:
        :param kwargs:
        :return: map object
        """
        url = '/instance-ip/{0}'.format(uuid)
        put_body = {'instance-ip': kwargs}
        resp, body = self.put(url, json.dumps(put_body))
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_instance_ip(self, uuid):
        """
        :param uuid:
        :return: map object
        """
        url = '/instance-ip/{0}'.format(uuid)
        resp, body = self.delete(url)
        return base.ResponseBody(resp, body)
