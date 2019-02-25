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
Tempest test-case to test analytics node objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class ContrailAnalyticsNodeTest(rbac_base.BaseContrailTest):
    """Test class to test analytics node objects using RBAC roles"""

    def _create_analytics_node(self):
        node_name = data_utils.rand_name('analytics-node')
        post_data = {
            'fq_name': ['default-global-system-config', node_name],
            'parent_type': 'global-system-config'
        }
        new_node = self.analytics_node_client.create_analytics_nodes(
            **post_data)['analytics-node']
        self.addCleanup(self._try_delete_resource,
                        self.analytics_node_client.delete_analytics_node,
                        new_node['uuid'])
        return new_node

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_analytics_nodes"])
    @decorators.idempotent_id('d3002e37-4b42-446d-b144-1b53f0dadfd3')
    def test_list_analytics_nodes(self):
        """test method for list analytics nodes"""
        with self.override_role():
            self.analytics_node_client.list_analytics_nodes()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_analytics_node"])
    @decorators.idempotent_id('b51043fd-77ba-4312-b96f-569ed5153338')
    def test_show_analytics_node(self):
        """test method for show analytics nodes"""
        new_node = self._create_analytics_node()
        with self.override_role():
            self.analytics_node_client.show_analytics_node(new_node['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_analytics_nodes"])
    @decorators.idempotent_id('c57482c9-fcb4-4f41-95b0-7f0ffeee3dc3')
    def test_create_analytics_nodes(self):
        """test method for create analytics nodes"""
        with self.override_role():
            self._create_analytics_node()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_analytics_node"])
    @decorators.idempotent_id('ff50a2df-6283-409e-ab03-c13b63acc8a0')
    def test_update_analytics_node(self):
        """test method for update analytics nodes"""
        new_node = self._create_analytics_node()
        update_name = data_utils.rand_name('updated_node')
        with self.override_role():
            self.analytics_node_client.update_analytics_node(
                new_node['uuid'], display_name=update_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_analytics_node"])
    @decorators.idempotent_id('972f997a-c89f-4227-8ae9-5a2335ec0b0a')
    def test_delete_analytics_node(self):
        """test method for delete analytics nodes"""
        new_node = self._create_analytics_node()
        with self.override_role():
            self.analytics_node_client.delete_analytics_node(new_node['uuid'])
