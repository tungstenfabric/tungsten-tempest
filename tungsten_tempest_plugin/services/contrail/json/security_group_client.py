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
Tempest service class for security group test cases
"""

from oslo_serialization import jsonutils as json
from tungsten_tempest_plugin.services.contrail.json import base


class SecurityGroupClient(base.BaseContrailClient):

    """
    Service class for security group test cases
    """

    def list_security_groups(self):
        """
        :return:
        """
        url = '/security-groups'
        return self.get(url)

    def show_security_group(self, sec_group_id):
        """
        :param sec_group_id:
        :return:
        """
        url = '/security-group/%s' % sec_group_id
        return self.get(url)

    def create_security_groups(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'security-group': kwargs})
        url = '/security-groups'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_security_group(self, sec_group_id, **kwargs):
        """
        :param sec_group_id:
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'security-group': kwargs})
        url = '/security-group/%s' % sec_group_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_security_group(self, sec_group_id):
        """
        :param sec_group_id:
        :return:
        """
        url = '/security-group/%s' % sec_group_id
        return self.delete(url)
