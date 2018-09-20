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
Tempest service class for route test cases
"""

from oslo_serialization import jsonutils as json
from tungsten_tempest_plugin.services.contrail.json import base


class RouteClient(base.BaseContrailClient):

    """
    Service class for route test cases
    """

    def list_route_tables(self):
        """
        :return:
        """
        url = '/route-tables'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_route_table(self, route_id):
        """
        :param route_id:
        :return:
        """
        url = '/route-table/%s' % route_id
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_route_tables(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'route-table': kwargs})
        url = 'route-tables'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_route_table(self, route_id, **kwargs):
        """
        :param route_id:
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'route-table': kwargs})
        url = '/route-table/%s' % route_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_route_table(self, route_id):
        """
        :param route_id:
        :return:
        """
        url = '/route-table/%s' % route_id
        resp, body = self.delete(url)
        return base.ResponseBody(resp, body)

    def list_interface_route_tables(self):
        """
        :return:
        """
        url = '/interface-route-tables'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_interface_route_table(self, interface_route_id):
        """
        :param interface_route_id:
        :return:
        """
        url = '/interface-route-table/%s' % interface_route_id
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_interface_route_tables(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'interface-route-table': kwargs})
        url = 'interface-route-tables'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_interface_route_table(self, interface_route_id, **kwargs):
        """
        :param interface_route_id:
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'interface-route-table': kwargs})
        url = '/interface-route-table/%s' % interface_route_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_interface_route_table(self, interface_route_id):
        """
        :param interface_route_id:
        :return:
        """
        url = '/interface-route-table/%s' % interface_route_id
        resp, body = self.delete(url)
        return base.ResponseBody(resp, body)

    def list_route_targets(self):
        """
        :return:
        """
        url = '/route-targets'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_route_target(self, route_target_id):
        """
        :param route_target_id:
        :return:
        """
        url = '/route-target/%s' % route_target_id
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_route_targets(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'route-target': kwargs})
        url = 'route-targets'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_route_target(self, route_target_id, **kwargs):
        """
        :param route_target_id:
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'route-target': kwargs})
        url = '/route-target/%s' % route_target_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_route_target(self, route_target_id):
        """
        :param route_target_id:
        :return:
        """
        url = '/route-target/%s' % route_target_id
        resp, body = self.delete(url)
        return base.ResponseBody(resp, body)

    def list_route_aggregates(self):
        """
        :return:
        """
        url = '/route-aggregates'
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_route_aggregate(self, route_aggr_id):
        """
        :param route_aggr_id:
        :return:
        """
        url = '/route-aggregate/%s' % route_aggr_id
        resp, body = self.get(url)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def create_route_aggregates(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'route-aggregate': kwargs})
        url = 'route-aggregates'
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def update_route_aggregate(self, route_aggr_id, **kwargs):
        """
        :param route_aggr_id:
        :param kwargs:
        :return:
        """
        post_body = json.dumps({'route-aggregate': kwargs})
        url = '/route-aggregate/%s' % route_aggr_id
        resp, body = self.put(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def delete_route_aggregate(self, route_aggr_id):
        """
        :param route_aggr_id:
        :return:
        """
        url = '/route-aggregate/%s' % route_aggr_id
        resp, body = self.delete(url)
        return base.ResponseBody(resp, body)
