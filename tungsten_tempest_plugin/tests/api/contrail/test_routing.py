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
Tempest test-case to test routing objects using RBAC roles
"""

from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF


class RoutingTest(rbac_base.BaseContrailTest):
    """Test class to test routing objects using RBAC roles"""

    @classmethod
    def resource_setup(cls):
        super(RoutingTest, cls).resource_setup()
        net_name = data_utils.rand_name('test-net')
        net_fq_name = ['default-domain', cls.tenant_name, net_name]
        cls.network = cls.vn_client.create_virtual_networks(
            parent_type='project',
            fq_name=net_fq_name)['virtual-network']

    @classmethod
    def resource_cleanup(cls):
        cls._try_delete_resource(cls.vn_client.delete_virtual_network,
                                 cls.network['uuid'])
        super(RoutingTest, cls).resource_cleanup()

    def _create_routing_instances(self):
        instance_name = data_utils.rand_name('test-instance')
        instance_fq_name = ['default-domain', self.tenant_name,
                            self.network['name'], instance_name]
        new_instance = self.routing_client.create_routing_instances(
            parent_type='virtual-network',
            fq_name=instance_fq_name)['routing-instance']
        self.addCleanup(self._try_delete_resource,
                        self.routing_client.delete_routing_instance,
                        new_instance['uuid'])
        return new_instance

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_routing_instances"])
    @decorators.idempotent_id('054c56ba-76b2-4161-a702-40301d8de085')
    def test_list_routing_instances(self):
        """test method for list routing instance objects"""
        with self.override_role():
            self.routing_client.list_routing_instances()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_routing_instances"])
    @decorators.idempotent_id('3d44a46b-5436-43a8-b2f7-8581f0f04dbc')
    def test_create_routing_instances(self):
        """test method for create routing instance objects"""
        with self.override_role():
            self._create_routing_instances()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_routing_instance"])
    @decorators.idempotent_id('161abb37-6037-422b-b453-108a5d10caca')
    def test_show_routing_instance(self):
        """test method for show routing instance objects"""
        new_instance = self._create_routing_instances()
        with self.override_role():
            self.routing_client.show_routing_instance(new_instance['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_routing_instance"])
    @decorators.idempotent_id('1d3af01e-01bf-4347-a9bc-633732339e0e')
    def test_delete_routing_instance(self):
        """test method for delete routing instance objects"""
        new_instance = self._create_routing_instances()
        with self.override_role():
            self.routing_client.delete_routing_instance(new_instance['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_routing_instance"])
    @decorators.idempotent_id('ebcfd442-2a26-4954-968b-e17e414ed0d1')
    def test_update_routing_instance(self):
        """test method for update routing instance objects"""
        new_instance = self._create_routing_instances()
        with self.override_role():
            self.routing_client.update_routing_instance(
                new_instance['uuid'],
                display_name=data_utils.rand_name('test-instance'))
