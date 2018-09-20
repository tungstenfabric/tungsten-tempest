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
Tempest service class for QoS test cases
"""

import json

from tungsten_tempest_plugin.services.contrail.json import base


class QosContrailClient(base.BaseContrailClient):

    """
    Service class for QoS test cases
    """

    def show_global_qos_config(self, instance_id):
        """
        :param instance_id:
        :return:
        """
        url = '/global-qos-config/%s' % instance_id
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_global_qos_config(self, instance_id):
        """
        :param instance_id:
        :return:
        """
        url = '/global-qos-config/%s' % instance_id
        return self.delete(url)

    def update_global_qos_config(self, instance_id, **kwargs):
        """
        :param instance_id:
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'global-qos-config': kwargs})
        url = '/global-qos-config/%s' % instance_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def list_global_qos_configs(self):
        """
        :return:
        """
        url = '/global-qos-configs'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_global_qos_configs(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'global-qos-config': kwargs})
        url = '/global-qos-configs'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_qos_config(self, qos_config_id):
        """
        :param qos_config_id:
        :return:
        """
        url = '/qos-config/%s' % qos_config_id
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_qos_config(self, qos_config_id):
        """
        :param qos_config_id:
        :return:
        """
        url = '/qos-config/%s' % qos_config_id
        return self.delete(url)

    def update_qos_config(self, qos_config_id, **kwargs):
        """
        :param qos_config_id:
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'qos-config': kwargs})
        url = '/qos-config/%s' % qos_config_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def list_qos_configs(self):
        """
        :return:
        """
        url = '/qos-configs'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_qos_configs(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'qos-config': kwargs})
        url = '/qos-configs'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_qos_queue(self, qos_queue_id):
        """
        :param qos_queue_id:
        :return:
        """
        url = '/qos-queue/%s' % qos_queue_id
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_qos_queue(self, qos_queue_id):
        """
        :param qos_queue_id:
        :return:
        """
        url = '/qos-queue/%s' % qos_queue_id
        return self.delete(url)

    def update_qos_queue(self, qos_queue_id, **kwargs):
        """
        :param qos_queue_id:
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'qos-queue': kwargs})
        url = '/qos-queue/%s' % qos_queue_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def list_qos_queues(self):
        """
        :return:
        """
        url = '/qos-queues'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_qos_queues(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'qos-queue': kwargs})
        url = '/qos-queues'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
