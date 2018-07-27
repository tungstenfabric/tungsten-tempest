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
Tempest service class for router test cases
"""

from oslo_serialization import jsonutils as json
from tungsten_tempest_plugin.services.contrail.json import base


class RouterClient(base.BaseContrailClient):

    """
    Service class for router test cases
    """

    def list_virtual_routers(self):
        """
        :return:
        """
        url = '/virtual-routers'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_virtual_router(self, vrouter_id):
        """
        :param vrouter_id:
        :return:
        """
        url = '/virtual-router/%s' % vrouter_id
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_virtual_routers(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'virtual-router': kwargs})
        url = '/virtual-routers'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_virtual_router(self, vrouter_id, **kwargs):
        """
        :param vrouter_id:
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'virtual-router': kwargs})
        url = '/virtual-router/%s' % vrouter_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_virtual_router(self, vrouter_id):
        """
        :param vrouter_id:
        :return:
        """
        url = '/virtual-router/%s' % vrouter_id
        resp, body = self.delete(url)
        return base.ResponseBody(resp, body)

    def list_global_vrouter_configs(self):
        """
        :return:
        """
        url = '/global-vrouter-configs'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_global_vrouter_config(self, global_vrouter_config_id):
        """
        :param global_vrouter_config_id:
        :return:
        """
        url = '/global-vrouter-config/%s' % global_vrouter_config_id
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_global_vrouter_configs(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'global-vrouter-config': kwargs})
        url = '/global-vrouter-configs'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_global_vrouter_config(self, global_vrouter_config_id, **kwargs):
        """
        :param global_vrouter_config_id:
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'global-vrouter-config': kwargs})
        url = '/global-vrouter-config/%s' % global_vrouter_config_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_global_vrouter_config(self, global_vrouter_config_id):
        """
        :param global_vrouter_config_id:
        :return:
        """
        url = '/global-vrouter-config/%s' % global_vrouter_config_id
        resp, body = self.delete(url)
        return base.ResponseBody(resp, body)

    def list_logical_routers(self):
        """
        :return:
        """
        url = '/logical-routers'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_logical_router(self, logical_router_id):
        """
        :param logical_router_id:
        :return:
        """
        url = '/logical-router/%s' % logical_router_id
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_logical_routers(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'logical-router': kwargs})
        url = '/logical-routers'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_logical_router(self, logical_router_id, **kwargs):
        """
        :param logical_router_id:
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'logical-router': kwargs})
        url = '/logical-router/%s' % logical_router_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_logical_router(self, logical_router_id):
        """
        :param logical_router_id:
        :return:
        """
        url = '/logical-router/%s' % logical_router_id
        resp, body = self.delete(url)
        return base.ResponseBody(resp, body)

    def list_bgp_routers(self):
        """
        :return:
        """
        url = '/bgp-routers'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_bgp_router(self, bgp_router_id):
        """
        :param bgp_router_id:
        :return:
        """
        url = '/bgp-router/%s' % bgp_router_id
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_bgp_routers(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'bgp-router': kwargs})
        url = '/bgp-routers'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_bgp_router(self, bgp_router_id, **kwargs):
        """
        :param bgp_router_id:
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'bgp-router': kwargs})
        url = '/bgp-router/%s' % bgp_router_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_bgp_router(self, bgp_router_id):
        """
        :param bgp_router_id:
        :return:
        """
        url = '/bgp-router/%s' % bgp_router_id
        resp, body = self.delete(url)
        return base.ResponseBody(resp, body)

    def list_physical_routers(self):
        """
        :return:
        """
        url = '/physical-routers'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_physical_router(self, physical_router_id):
        """
        :param physical_router_id:
        :return:
        """
        url = '/physical-router/%s' % physical_router_id
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_physical_routers(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'physical-router': kwargs})
        url = '/physical-routers'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_physical_router(self, physical_router_id, **kwargs):
        """
        :param physical_router_id:
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'physical-router': kwargs})
        url = '/physical-router/%s' % physical_router_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_physical_router(self, physical_router_id):
        """
        :param physical_router_id:
        :return:
        """
        url = '/physical-router/%s' % physical_router_id
        resp, body = self.delete(url)
        return base.ResponseBody(resp, body)
