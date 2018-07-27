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
Tempest service class for config test cases
"""

from oslo_serialization import jsonutils as json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class ConfigClient(base.BaseContrailClient):

    """
    Service class for config test cases
    """

    # Below are client codes for global-system-config APIs
    def list_global_system_configs(self, params=None):
        """
        :param params:
        :return: response object
        """
        url = '/global-system-configs'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_global_system_configs(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/global-system-configs'
        post_body = json.dumps({'global-system-config': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_global_system_config(self, template_id):
        """
        :param template_id:
        :return: response object
        """
        url = '/global-system-config/%s' % str(template_id)
        return self.get(url)

    def delete_global_system_config(self, template_id):
        """
        :param template_id:
        :return: response object
        """
        url = '/global-system-config/%s' % str(template_id)
        return self.delete(url)

    def update_global_system_config(self, template_id, **kwargs):
        """
        :param template_id:
        :param kwargs:
        :return: map object
        """
        url = '/global-system-config/%s' % str(template_id)
        put_data = {'global-system-config': kwargs}
        req_put_data = json.dumps(put_data)
        resp, body = self.put(url, req_put_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    # Below are client codes for config-node APIs
    def list_config_nodes(self):
        """
        :return: map object
        """
        url = '/config-nodes'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_config_nodes(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/config-nodes'
        post_body = json.dumps({'config-node': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_config_node(self, node_id):
        """
        :param node_id:
        :return: response object
        """
        url = '/config-node/%s' % str(node_id)
        return self.delete(url)

    def show_config_node(self, node_id):
        """
        :param node_id:
        :return: response object
        """
        url = '/config-node/%s' % str(node_id)
        return self.get(url)

    def update_config_node(self, node_id, **kwargs):
        """
        :param node_id:
        :param kwargs:
        :return: map object
        """
        url = '/config-node/%s' % str(node_id)
        put_data = {'config-node': kwargs}
        req_put_data = json.dumps(put_data)
        resp, body = self.put(url, req_put_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    # Below are client codes for config-root APIs
    def list_config_roots(self):
        """
        :return: map object
        """
        url = '/config-roots'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_config_roots(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/config-roots'
        post_body = json.dumps({'config-root': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_config_root(self, root_id):
        """
        :param root_id:
        :return: response object
        """
        url = '/config-root/%s' % str(root_id)
        return self.delete(url)

    def show_config_root(self, root_id):
        """
        :param root_id:
        :return: response object
        """
        url = '/config-root/%s' % str(root_id)
        return self.get(url)

    def update_config_root(self, root_id, **kwargs):
        """
        :param root_id:
        :param kwargs:
        :return: map object
        """
        url = '/config-root/%s' % str(root_id)
        put_data = {'config-root': kwargs}
        req_put_data = json.dumps(put_data)
        resp, body = self.put(url, req_put_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
