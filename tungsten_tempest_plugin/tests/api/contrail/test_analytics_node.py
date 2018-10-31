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

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

from patrole_tempest_plugin import rbac_rule_validation

from tempest import config
from tempest.lib import decorators
from tempest.lib.common.utils import data_utils
from tempest.lib.decorators import idempotent_id

CONF = config.CONF
LOG = logging.getLogger(__name__)


class ContrailAnalyticsNodeTest(rbac_base.BaseContrailTest):

    """
    Test class to test analytics node objects using RBAC roles
    """

    def _create_global_system_config(self):
        config_name = data_utils.rand_name('test-config')
        parent_type = 'config-root'
        config_fq_name = [config_name]
        new_config = \
            self.config_client.create_global_system_configs(
                parent_type=parent_type,
                display_name=config_name,
                fq_name=config_fq_name)['global-system-config']
        self.addCleanup(self._try_delete_resource,
                        (self.config_client.
                         delete_global_system_config),
                        new_config['uuid'])
        return new_config

    def _create_analytics_node(self, global_system_config):
        node_name = data_utils.rand_name('analytics-node')
        post_data = {
            'fq_name': [global_system_config, node_name],
            'parent_type': 'global-system-config'
        }
        new_node = self.analytics_node_client.create_analytics_nodes(
            **post_data)['analytics-node']
        self.addCleanup(self._try_delete_resource,
                        self.analytics_node_client.delete_analytics_node,
                        new_node['uuid'])
        return new_node

    @decorators.idempotent_id('6dbda64e-f575-4bb8-8600-b8a510e4ae96')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_analytics_nodes")
    @idempotent_id('d3002e37-4b42-446d-b144-1b53f0dadfd3')
    def test_list_analytics_nodes(self):
        """
        test method for list analytics nodes
        """
        with self.rbac_utils.override_role(self):
            self.analytics_node_client.list_analytics_nodes()

    @decorators.idempotent_id('0852bb86-6a95-476d-a964-79e73b08b839')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_analytics_node")
    @idempotent_id('b51043fd-77ba-4312-b96f-569ed5153338')
    def test_show_analytics_node(self):
        """
        test method for show analytics nodes
        """
        # create global system config
        global_system_config = self._create_global_system_config()['name']
        new_node = self._create_analytics_node(global_system_config)
        with self.rbac_utils.override_role(self):
            self.analytics_node_client.show_analytics_node(new_node['uuid'])

    @decorators.idempotent_id('a1a09763-b56b-4caf-b9d5-6d95d416dfc4')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_analytics_nodes")
    @idempotent_id('c57482c9-fcb4-4f41-95b0-7f0ffeee3dc3')
    def test_create_analytics_nodes(self):
        """
        test method for create analytics nodes
        """
        # create global system config
        global_system_config = self._create_global_system_config()['name']
        with self.rbac_utils.override_role(self):
            self._create_analytics_node(global_system_config)

    @decorators.idempotent_id('67437d99-c5b1-4d42-8a91-251c4055d4c1')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_analytics_node")
    @idempotent_id('ff50a2df-6283-409e-ab03-c13b63acc8a0')
    def test_update_analytics_node(self):
        """
        test method for update analytics nodes
        """
        # create global system config
        global_system_config = self._create_global_system_config()['name']
        new_node = self._create_analytics_node(global_system_config)
        update_name = data_utils.rand_name('updated_node')
        with self.rbac_utils.override_role(self):
            self.analytics_node_client.update_analytics_node(
                new_node['uuid'], display_name=update_name)

    @decorators.idempotent_id('7d62d6cc-dcd9-49e0-85e6-6115e8228ac0')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_analytics_node")
    @idempotent_id('972f997a-c89f-4227-8ae9-5a2335ec0b0a')
    def test_delete_analytics_node(self):
        """
        test method for delete analytics nodes
        """
        # create global system config
        global_system_config = self._create_global_system_config()['name']
        new_node = self._create_analytics_node(global_system_config)
        with self.rbac_utils.override_role(self):
            self.analytics_node_client.delete_analytics_node(new_node['uuid'])
