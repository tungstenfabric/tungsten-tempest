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
Tempest test-case to test virtual network objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class NetworksTest(rbac_base.BaseContrailTest):
    """Test class to test vm network using RBAC roles"""

    @classmethod
    def resource_setup(cls):
        super(NetworksTest, cls).resource_setup()

        # Create virtual network for tests
        net_name = data_utils.rand_name('rbac-virtual-network')
        fq_name = ['default-domain', cls.tenant_name, net_name]
        post_body = {'parent_type': 'project',
                     'router_external': True,
                     'fq_name': fq_name}
        cls.network = cls.vn_client.create_virtual_networks(
            **post_body)['virtual-network']

    @classmethod
    def resource_cleanup(cls):

        cls._try_delete_resource(cls.vn_client.delete_virtual_network,
                                 cls.network['uuid'])
        super(NetworksTest, cls).resource_cleanup()

    def _create_virtual_network(self):
        net_name = data_utils.rand_name('rbac-virtual-network')
        fq_name = ['default-domain', self.tenant_name, net_name]
        post_body = {'parent_type': 'project',
                     'router_external': True,
                     'fq_name': fq_name}
        network = self.vn_client.create_virtual_networks(
            **post_body)['virtual-network']
        self.addCleanup(self._try_delete_resource,
                        self.vn_client.delete_virtual_network,
                        network['uuid'])
        return network

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_virtual_networks"])
    @decorators.idempotent_id('375ebc8d-dc52-4d9c-877b-85aba35b1539')
    def test_list_virtual_networks(self):
        """test method for list vm network objects"""
        with self.override_role():
            self.vn_client.list_virtual_networks()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_virtual_networks"])
    @decorators.idempotent_id('375ebc8d-dc52-4d9c-877b-96aba35b2530')
    def test_create_virtual_networks(self):
        """test method for create vm network objects"""
        with self.override_role():
            self._create_virtual_network()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_virtual_network"])
    @decorators.idempotent_id('375ebc8d-dc52-4d9c-566b-150a025c1237')
    def test_update_virtual_network(self):
        """test method for update vm network objects"""
        # Create virtual network
        uuid = self._create_virtual_network()['uuid']
        with self.override_role():
            self.vn_client.update_virtual_network(
                uuid, router_external=False)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_virtual_network"])
    @decorators.idempotent_id('375ebc8d-dc52-4d9c-877b-17bcb53c3641')
    def test_delete_virtual_network(self):
        """test method for delete vm network objects"""
        uuid = self._create_virtual_network()['uuid']
        with self.override_role():
            self.vn_client.delete_virtual_network(uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_virtual_network"])
    @decorators.idempotent_id('375ebc8d-dc52-4d9c-877b-27c1a1242a81')
    def test_show_virtual_network(self):
        """test method for show vm network objects"""
        uuid = self._create_virtual_network()['uuid']
        with self.override_role():
            self.vn_client.show_virtual_network(uuid)
