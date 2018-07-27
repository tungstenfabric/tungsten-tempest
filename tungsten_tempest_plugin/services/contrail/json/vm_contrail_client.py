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
Tempest service class for virtual machine test cases
"""

import json
from tungsten_tempest_plugin.services.contrail.json import base


class VmContrailClient(base.BaseContrailClient):

    """
    Service class for vm test cases
    """

    def list_virtual_machine_interfaces(self):
        """
        :return:
        """
        url = '/virtual-machine-interfaces'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_vm_interfaces(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'virtual-machine-interface': kwargs})
        url = '/virtual-machine-interfaces'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_virtual_machine_interface(self, instance_id):
        """
        :param instance_id:
        :return:
        """
        url = '/virtual-machine-interface/%s' % instance_id
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_vm_interface(self, instance_id):
        """
        :param instance_id:
        :return:
        """
        url = '/virtual-machine-interface/%s' % instance_id
        return self.delete(url)

    def update_vm_interface(self, instance_id, **kwargs):
        """
        :param instance_id:
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'virtual-machine-interface': kwargs})
        url = '/virtual-machine-interface/%s' % instance_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
