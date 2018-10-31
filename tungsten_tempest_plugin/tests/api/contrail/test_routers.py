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
Tempest test-case to test project objects using RBAC roles
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


class BaseRouterTest(rbac_base.BaseContrailTest):

    """
    Test class to test router objects using RBAC roles
    """

    @classmethod
    def resource_setup(cls):
        super(BaseRouterTest, cls).resource_setup()
        net_name = data_utils.rand_name('test-net')
        net_fq_name = ['default-domain', cls.tenant_name, net_name]
        cls.network = cls.vn_client.create_virtual_networks(
            parent_type='project',
            fq_name=net_fq_name)['virtual-network']

    @classmethod
    def resource_cleanup(cls):
        cls._try_delete_resource(cls.vn_client.delete_virtual_network,
                                 cls.network['uuid'])
        super(BaseRouterTest, cls).resource_cleanup()

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

    def _create_physical_router(self, global_system_config):
        fq_name = data_utils.rand_name('physical-router-template')
        post_body = {
            'parent_type': 'global-system-config',
            'fq_name': [global_system_config, fq_name]}
        router = self.router_client.create_physical_routers(
            **post_body)['physical-router']
        self.addCleanup(self._try_delete_resource,
                        self.router_client.delete_physical_router,
                        router['uuid'])
        return router

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
        LOG.debug("INSTANCE %s ", new_instance)
        return new_instance

    def _create_bgp_router(self, instance):
        fq_name = data_utils.rand_name('bgp-router-template')
        post_body = {
            'parent_type': 'routing-instance',
            'fq_name': ['default-domain', self.tenant_name,
                        self.network['name'], instance['name'], fq_name]}
        router = self.router_client.create_bgp_routers(
            **post_body)['bgp-router']
        self.addCleanup(self._try_delete_resource,
                        self.router_client.delete_bgp_router,
                        router['uuid'])
        return router

    def _create_global_vrouter_config(self, global_system_config):
        fq_name = data_utils.rand_name('global-vrouter-config-template')
        post_body = {
            'parent_type': 'global-system-config',
            'fq_name': [global_system_config, fq_name]}
        router = self.router_client.create_global_vrouter_configs(
            **post_body)['global-vrouter-config']
        self.addCleanup(self._try_delete_resource,
                        self.router_client.delete_global_vrouter_config,
                        router['uuid'])
        return router

    def _create_logical_router(self):
        fq_name = data_utils.rand_name('logical-router-template')
        post_body = {
            'parent_type': 'project',
            'fq_name': ['default-domain', self.tenant_name, fq_name]}
        router = self.router_client.create_logical_routers(
            **post_body)['logical-router']
        self.addCleanup(self._try_delete_resource,
                        self.router_client.delete_logical_router,
                        router['uuid'])
        return router

    def _create_virtual_router(self, global_system_config):
        fq_name = data_utils.rand_name('virtual-router-template')
        post_body = {
            'parent_type': 'global-system-config',
            'fq_name': [global_system_config, fq_name]}
        router = self.router_client.create_virtual_routers(
            **post_body)['virtual-router']
        self.addCleanup(self._try_delete_resource,
                        self.router_client.delete_virtual_router,
                        router['uuid'])
        return router

    @decorators.idempotent_id('7cbbf934-91e4-4243-a0d8-09798b92e1a2')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_physical_routers")
    @idempotent_id('349ac042-b922-4727-9e1b-8f363ee343f3')
    def test_list_physical_routers(self):
        """
        test method for list physical router objects
        """
        with self.rbac_utils.override_role(self):
            self.router_client.list_physical_routers()

    @decorators.idempotent_id('7f24af6e-b577-440e-87be-23809260bcc8')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_physical_routers")
    @idempotent_id('d0b7449e-9037-4f9f-8c7e-9f364c95f18a')
    def test_create_physical_routers(self):
        """
        test method for create physical router objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        with self.rbac_utils.override_role(self):
            self._create_physical_router(global_system_config)

    @decorators.idempotent_id('ba07818c-c572-459a-a3c8-2bbc1fbe485e')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_physical_router")
    @idempotent_id('6dfc53f4-a884-46d5-b303-22ba59c116f4')
    def test_show_physical_router(self):
        """
        test method for show physical router objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        physical_router_uuid = self._create_physical_router(
            global_system_config)['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.show_physical_router(physical_router_uuid)

    @decorators.idempotent_id('0dbc0f15-1d61-4aa4-a9bd-4e060335b960')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_physical_router")
    @idempotent_id('c270f369-8cd7-4ee3-8ab1-4580c3138a5c')
    def test_update_physical_router(self):
        """
        test method for update physical router objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        updated_fq_name = data_utils.rand_name('rbac-physical-router-new-name')
        physical_router_uuid = self._create_physical_router(
            global_system_config)['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.update_physical_router(
                physical_router_uuid,
                display_name=updated_fq_name)

    @decorators.idempotent_id('7e92cc5c-1b2f-48cf-8b4d-499244866dff')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_physical_router")
    @idempotent_id('eeded742-6a8d-4e88-bfa8-fe32db463c53')
    def test_delete_physical_router(self):
        """
        test method for delete physical router objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        physical_router_uuid = self._create_physical_router(
            global_system_config)['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.delete_physical_router(physical_router_uuid)

    @decorators.idempotent_id('964f0f98-5447-4eb7-b6ca-e1be9c57732e')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_bgp_routers")
    @idempotent_id('49bfb461-f99e-4585-b051-e20a3c937589')
    def test_list_bgp_routers(self):
        """
        test method for list bgp router objects
        """
        with self.rbac_utils.override_role(self):
            self.router_client.list_bgp_routers()

    @decorators.idempotent_id('f44e0191-997e-410e-84e6-fc99c1b93598')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_bgp_routers")
    @idempotent_id('7567974c-040e-4edd-b3a1-c633aa9651cb')
    def test_create_bgp_routers(self):
        """
        test method for create bgp router objects
        """
        # Create Routing Instance
        routing_instance = self._create_routing_instances()
        with self.rbac_utils.override_role(self):
            self._create_bgp_router(routing_instance)

    @decorators.idempotent_id('a0eb42de-1a3d-47aa-a0d3-37ebb6614b41')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_bgp_router")
    @idempotent_id('0d3ad424-18c9-4d96-8708-fa1ebd45594b')
    def test_show_bgp_router(self):
        """
        test method for show bgp router objects
        """
        # Create Routing Instance
        routing_instance = self._create_routing_instances()
        bgp_router_uuid = self._create_bgp_router(routing_instance)['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.show_bgp_router(bgp_router_uuid)

    @decorators.idempotent_id('e28f5741-bce5-48d8-9933-d0e38b6a122e')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_bgp_router")
    @idempotent_id('dc50e7c5-7614-4281-8a66-282c52f3c769')
    def test_update_bgp_router(self):
        """
        test method for update bgp router objects
        """
        # Create Routing Instance
        routing_instance = self._create_routing_instances()
        updated_fq_name = data_utils.rand_name('rbac-bgp-router-new-name')
        bgp_router_uuid = self._create_bgp_router(routing_instance)['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.update_bgp_router(
                bgp_router_uuid,
                display_name=updated_fq_name)

    @decorators.idempotent_id('862b2de5-2660-4a2a-9732-d6ea3ab88eff')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_bgp_router")
    @idempotent_id('f14aee72-cad4-4c3e-8eea-7886a81abb24')
    def test_delete_bgp_router(self):
        """
        test method for delete bgp router objects
        """
        # Create Routing Instance
        routing_instance = self._create_routing_instances()
        bgp_router_uuid = self._create_bgp_router(routing_instance)['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.delete_bgp_router(bgp_router_uuid)

    @decorators.idempotent_id('73001d40-3127-4a99-a7d0-eb59f76fd35b')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_global_vrouter_configs")
    @idempotent_id('4af768d1-3cbe-4aff-bcbc-0e045cac3277')
    def test_list_global_vrouter(self):
        """
        test method for list global vrouter config objects
        """
        with self.rbac_utils.override_role(self):
            self.router_client.list_global_vrouter_configs()

    @decorators.idempotent_id('d37d7324-fc8a-43e0-825e-ed979341be3c')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_global_vrouter_configs")
    @idempotent_id('e13d800f-9304-4a06-9bf1-ad08345a13a8')
    def test_create_global_vrouter(self):
        """
        test method for create global vrouter config objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        with self.rbac_utils.override_role(self):
            self._create_global_vrouter_config(global_system_config)

    @decorators.idempotent_id('620294a4-a597-4881-836a-3cc08eb3c464')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_global_vrouter_config")
    @idempotent_id('3bb6f4e1-fd3f-4338-8392-f7f80974a80e')
    def test_show_global_vrouter_config(self):
        """
        test method for show global vrouter config objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        global_vrouter_config_uuid = self._create_global_vrouter_config(
            global_system_config)['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.show_global_vrouter_config(
                global_vrouter_config_uuid)

    @decorators.idempotent_id('92fae487-86ab-492d-86fd-c06963ce5ea6')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_global_vrouter_config")
    @idempotent_id('36fcdd51-c42b-4e67-8c26-73d4cde47507')
    def test_update_global_vrouter(self):
        """
        test method for update global vrouter config objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        updated_fq_name = data_utils.rand_name(
            'rbac-global-vrouter-config-new-name')
        global_vrouter_config_uuid = self._create_global_vrouter_config(
            global_system_config)['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.update_global_vrouter_config(
                global_vrouter_config_uuid,
                display_name=updated_fq_name)

    @decorators.idempotent_id('945f1ddd-d787-4d93-b156-ec86267a2aca')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_global_vrouter_config")
    @idempotent_id('4f3d59e8-3dac-4346-9d13-5ebe5ad8f6cf')
    def test_delete_global_vrouter(self):
        """
        test method for delete global vrouter config objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        global_vrouter_config_uuid = self._create_global_vrouter_config(
            global_system_config)['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.delete_global_vrouter_config(
                global_vrouter_config_uuid)

    @decorators.idempotent_id('279dca60-f6e4-4dc2-8568-03d186e64086')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_logical_routers")
    @idempotent_id('674bf3de-a9e5-45c2-921b-b89db73a2abe')
    def test_list_logical_routers(self):
        """
        test method for list logical router objects
        """
        with self.rbac_utils.override_role(self):
            self.router_client.list_logical_routers()

    @decorators.idempotent_id('e2a3bd03-4573-4676-90f6-9e66dd05dad6')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_logical_routers")
    @idempotent_id('610f051b-8eba-4d3a-ba43-91386bfc0e52')
    def test_create_logical_routers(self):
        """
        test method for create logical router objects
        """
        with self.rbac_utils.override_role(self):
            self._create_logical_router()

    @decorators.idempotent_id('1c4274ce-31d7-45c7-94ab-7026d4c456d2')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_logical_router")
    @idempotent_id('992841d4-0d5d-4d85-b513-049b33e2a2e2')
    def test_show_logical_router(self):
        """
        test method for show logical router objects
        """
        logical_router_uuid = self._create_logical_router()['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.show_logical_router(logical_router_uuid)

    @decorators.idempotent_id('6faeb2a2-e833-4d39-9db1-0e06b0507f0b')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_logical_router")
    @idempotent_id('518197bf-5233-4059-9021-5d7ecc74718e')
    def test_update_logical_router(self):
        """
        test method for update logical router objects
        """
        updated_fq_name = data_utils.rand_name('rbac-logical-router-new-name')
        logical_router_uuid = self._create_logical_router()['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.update_logical_router(
                logical_router_uuid,
                display_name=updated_fq_name)

    @decorators.idempotent_id('4ff3591c-f57f-4842-b74a-c0a2b8171c3f')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_logical_router")
    @idempotent_id('70448b9c-4444-45e0-b307-7bff4dc075b1')
    def test_delete_logical_router(self):
        """
        test method for delete logical router objects
        """
        logical_router_uuid = self._create_logical_router()['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.delete_logical_router(logical_router_uuid)

    @decorators.idempotent_id('5662ac7f-5a18-476d-a3c9-cc7c784f9dfa')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_virtual_routers")
    @idempotent_id('604dc476-732e-4890-8665-a497360f5475')
    def test_list_virtual_routers(self):
        """
        test method for list virtual router objects
        """
        with self.rbac_utils.override_role(self):
            self.router_client.list_virtual_routers()

    @decorators.idempotent_id('6d2b364c-cdb8-4de1-bc15-5f7d0b1533d2')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_virtual_routers")
    @idempotent_id('114beb14-45c0-4714-a407-d160bb102022')
    def test_create_virtual_routers(self):
        """
        test method for create virtual router objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        with self.rbac_utils.override_role(self):
            self._create_virtual_router(global_system_config)

    @decorators.idempotent_id('d9319e7f-8811-43e5-93ce-734ac7fb4f79')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_virtual_router")
    @idempotent_id('258fe4e0-3e39-460f-aafa-e3b53c96e534')
    def test_show_virtual_router(self):
        """
        test method for show virtual router objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        virtual_router_uuid = self._create_virtual_router(
            global_system_config)['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.show_virtual_router(virtual_router_uuid)

    @decorators.idempotent_id('4baa6195-bacd-4211-ab93-abd6ebbfe5d6')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_virtual_router")
    @idempotent_id('d1c72191-2068-4552-a78f-038cdd4c9c1d')
    def test_update_virtual_router(self):
        """
        test method for update virtual router objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        updated_fq_name = data_utils.rand_name('rbac-virtual-router-new-name')
        virtual_router_uuid = self._create_virtual_router(
            global_system_config)['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.update_virtual_router(
                virtual_router_uuid,
                display_name=updated_fq_name)

    @decorators.idempotent_id('bb7e4a21-1c8a-4a38-997c-612de0a4ee53')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_virtual_router")
    @idempotent_id('efbe25d6-8763-42d4-baf6-9f342e710144')
    def test_delete_virtual_router(self):
        """
        test method for delete virtual router objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        virtual_router_uuid = self._create_virtual_router(
            global_system_config)['uuid']
        with self.rbac_utils.override_role(self):
            self.router_client.delete_virtual_router(virtual_router_uuid)
