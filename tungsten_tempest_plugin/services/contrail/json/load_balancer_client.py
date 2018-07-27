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
Tempest service class for load balancer test cases
"""

import json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class LoadBalancerClient(base.BaseContrailClient):

    """
    Service class for load balancer test cases
    """

    def list_load_balancers(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/loadbalancers'
        if params:
            url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_load_balancers(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/loadbalancers'
        resp, body = self.post(url, json.dumps({'loadbalancer': kwargs}))
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_load_balancer(self, uuid, params=None):
        """
        :param uuid:
        :param params:
        :return:
        """
        url = '/loadbalancer/{0}'.format(uuid)
        if params:
            url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_load_balancer(self, uuid, **kwargs):
        """
        :param uuid:
        :param kwargs:
        :return:
        """
        url = '/loadbalancer/{0}'.format(uuid)
        resp, body = self.put(url, json.dumps({'loadbalancer': kwargs}))
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_load_balancer(self, uuid):
        """
        :param uuid:
        :return:
        """
        url = '/loadbalancer/{0}'.format(uuid)
        return self.delete(url)

    def list_lb_healthmonitors(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/loadbalancer-healthmonitors'
        if params:
            url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_lb_healthmonitors(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/loadbalancer-healthmonitors'
        resp, body = self.post(url, json.dumps(
            {'loadbalancer-healthmonitor': kwargs}))
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_lb_healthmonitor(self, uuid, params=None):
        """
        :param uuid:
        :param params:
        :return:
        """
        url = '/loadbalancer-healthmonitor/{0}'.format(uuid)
        if params:
            url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_lb_healthmonitor(self, uuid, **kwargs):
        """
        :param uuid:
        :param kwargs:
        :return:
        """
        url = '/loadbalancer-healthmonitor/{0}'.format(uuid)
        resp, body = self.put(url, json.dumps(
            {'loadbalancer-healthmonitor': kwargs}))
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_lb_healthmonitor(self, uuid):
        """
        :param uuid:
        :return:
        """
        url = '/loadbalancer-healthmonitor/{0}'.format(uuid)
        return self.delete(url)

    def list_load_balancer_listeners(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/loadbalancer-listeners'
        if params:
            url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_load_balancer_listeners(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/loadbalancer-listeners'
        resp, body = self.post(url, json.dumps(
            {'loadbalancer-listener': kwargs}))
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_load_balancer_listener(self, uuid, params=None):
        """
        :param uuid:
        :param params:
        :return:
        """
        url = '/loadbalancer-listener/{0}'.format(uuid)
        if params:
            url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_load_balancer_listener(self, uuid, **kwargs):
        """
        :param uuid:
        :param kwargs:
        :return:
        """
        url = '/loadbalancer-listener/{0}'.format(uuid)
        resp, body = self.put(url, json.dumps(
            {'loadbalancer-listener': kwargs}))
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_load_balancer_listener(self, uuid):
        """
        :param uuid:
        :return:
        """
        url = '/loadbalancer-listener/{0}'.format(uuid)
        return self.delete(url)

    def list_load_balancer_pools(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/loadbalancer-pools'
        if params:
            url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_load_balancer_pools(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/loadbalancer-pools'
        resp, body = self.post(url, json.dumps(
            {'loadbalancer-pool': kwargs}))
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_load_balancer_pool(self, uuid, params=None):
        """
        :param uuid:
        :param params:
        :return:
        """
        url = '/loadbalancer-pool/{0}'.format(uuid)
        if params:
            url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_load_balancer_pool(self, uuid, **kwargs):
        """
        :param uuid:
        :param kwargs:
        :return:
        """
        url = '/loadbalancer-pool/{0}'.format(uuid)
        resp, body = self.put(url, json.dumps(
            {'loadbalancer-pool': kwargs}))
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_load_balancer_pool(self, uuid):
        """
        :param uuid:
        :return:
        """
        url = '/loadbalancer-pool/{0}'.format(uuid)
        return self.delete(url)

    def list_load_balancer_members(self, params=None):
        """
        :param params:
        :return:
        """
        url = '/loadbalancer-members'
        if params:
            url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_load_balancer_members(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        url = '/loadbalancer-members'
        resp, body = self.post(url, json.dumps(
            {'loadbalancer-member': kwargs}))
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_load_balancer_member(self, uuid, params=None):
        """
        :param uuid:
        :param params:
        :return:
        """
        url = '/loadbalancer-member/{0}'.format(uuid)
        if params:
            url += '?%s' % urllib.urlencode(params)
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_load_balancer_member(self, uuid, **kwargs):
        """
        :param uuid:
        :param kwargs:
        :return:
        """
        url = '/loadbalancer-member/{0}'.format(uuid)
        resp, body = self.put(url, json.dumps(
            {'loadbalancer-member': kwargs}))
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_load_balancer_member(self, uuid):
        """
        :param uuid:
        :return:
        """
        url = '/loadbalancer-member/{0}'.format(uuid)
        return self.delete(url)
