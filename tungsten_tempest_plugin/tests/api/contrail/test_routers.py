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
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class BaseRouterTest(rbac_base.BaseContrailTest):
    """Test class to test router objects using RBAC roles"""

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

    def _create_physical_router(self):
        fq_name = data_utils.rand_name('physical-router-template')
        post_body = {
            'parent_type': 'global-system-config',
            'fq_name': ['default-global-system-config', fq_name]}
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

    def _create_global_vrouter_config(self):
        fq_name = data_utils.rand_name('global-vrouter-config-template')
        post_body = {
            'parent_type': 'global-system-config',
            'fq_name': ['default-global-system-config', fq_name]}
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

    def _create_virtual_router(self):
        fq_name = data_utils.rand_name('virtual-router-template')
        post_body = {
            'parent_type': 'global-system-config',
            'fq_name': ['default-global-system-config', fq_name]}
        router = self.router_client.create_virtual_routers(
            **post_body)['virtual-router']
        self.addCleanup(self._try_delete_resource,
                        self.router_client.delete_virtual_router,
                        router['uuid'])
        return router

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_physical_routers"])
    @decorators.idempotent_id('349ac042-b922-4727-9e1b-8f363ee343f3')
    def test_list_physical_routers(self):
        """test method for list physical router objects"""
        with self.override_role():
            self.router_client.list_physical_routers()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_physical_routers"])
    @decorators.idempotent_id('d0b7449e-9037-4f9f-8c7e-9f364c95f18a')
    def test_create_physical_routers(self):
        """test method for create physical router objects"""
        with self.override_role():
            self._create_physical_router()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_physical_router"])
    @decorators.idempotent_id('6dfc53f4-a884-46d5-b303-22ba59c116f4')
    def test_show_physical_router(self):
        """test method for show physical router objects"""
        physical_router_uuid = self._create_physical_router()['uuid']
        with self.override_role():
            self.router_client.show_physical_router(physical_router_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_physical_router"])
    @decorators.idempotent_id('c270f369-8cd7-4ee3-8ab1-4580c3138a5c')
    def test_update_physical_router(self):
        """test method for update physical router objects"""
        updated_fq_name = data_utils.rand_name('rbac-physical-router-new-name')
        physical_router_uuid = self._create_physical_router()['uuid']
        with self.override_role():
            self.router_client.update_physical_router(
                physical_router_uuid,
                display_name=updated_fq_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_physical_router"])
    @decorators.idempotent_id('eeded742-6a8d-4e88-bfa8-fe32db463c53')
    def test_delete_physical_router(self):
        """test method for delete physical router objects"""
        physical_router_uuid = self._create_physical_router()['uuid']
        with self.override_role():
            self.router_client.delete_physical_router(physical_router_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_bgp_routers"])
    @decorators.idempotent_id('49bfb461-f99e-4585-b051-e20a3c937589')
    def test_list_bgp_routers(self):
        """test method for list bgp router objects"""
        with self.override_role():
            self.router_client.list_bgp_routers()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_bgp_routers"])
    @decorators.idempotent_id('7567974c-040e-4edd-b3a1-c633aa9651cb')
    def test_create_bgp_routers(self):
        """test method for create bgp router objects"""
        # Create Routing Instance
        routing_instance = self._create_routing_instances()
        with self.override_role():
            self._create_bgp_router(routing_instance)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_bgp_router"])
    @decorators.idempotent_id('0d3ad424-18c9-4d96-8708-fa1ebd45594b')
    def test_show_bgp_router(self):
        """test method for show bgp router objects"""
        # Create Routing Instance
        routing_instance = self._create_routing_instances()
        bgp_router_uuid = self._create_bgp_router(routing_instance)['uuid']
        with self.override_role():
            self.router_client.show_bgp_router(bgp_router_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_bgp_router"])
    @decorators.idempotent_id('dc50e7c5-7614-4281-8a66-282c52f3c769')
    def test_update_bgp_router(self):
        """test method for update bgp router objects"""
        # Create Routing Instance
        routing_instance = self._create_routing_instances()
        updated_fq_name = data_utils.rand_name('rbac-bgp-router-new-name')
        bgp_router_uuid = self._create_bgp_router(routing_instance)['uuid']
        with self.override_role():
            self.router_client.update_bgp_router(
                bgp_router_uuid,
                display_name=updated_fq_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_bgp_router"])
    @decorators.idempotent_id('f14aee72-cad4-4c3e-8eea-7886a81abb24')
    def test_delete_bgp_router(self):
        """test method for delete bgp router objects"""
        # Create Routing Instance
        routing_instance = self._create_routing_instances()
        bgp_router_uuid = self._create_bgp_router(routing_instance)['uuid']
        with self.override_role():
            self.router_client.delete_bgp_router(bgp_router_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_global_vrouter_configs"])
    @decorators.idempotent_id('4af768d1-3cbe-4aff-bcbc-0e045cac3277')
    def test_list_global_vrouter_configs(self):
        """test method for list global vrouter config objects"""
        with self.override_role():
            self.router_client.list_global_vrouter_configs()

    @decorators.skip_because(bug="1792446")
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_global_vrouter_configs"])
    @decorators.idempotent_id('e13d800f-9304-4a06-9bf1-ad08345a13a8')
    def test_create_global_vrouter_configs(self):
        """test method for create global vrouter config objects"""
        # This test may make your environment unstable
        # Juniper JTAC 2018-0912-0503
        #
        # Creating a global-vrouter-config object with parent as
        # default-gloabl-system-config in a deployed environment makes vrouter
        # linklocal metadata to go missing.
        # vrouter-agent will stuck in Init state with "No configuration for
        # self" error.
        with self.override_role():
            self._create_global_vrouter_config()

    @decorators.skip_because(bug="1792446")
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_global_vrouter_config"])
    @decorators.idempotent_id('3bb6f4e1-fd3f-4338-8392-f7f80974a80e')
    def test_show_global_vrouter_config(self):
        """test method for show global vrouter config objects"""
        # This test may make your environment unstable
        # Juniper JTAC 2018-0912-0503
        #
        # Creating a global-vrouter-config object with parent as
        # default-gloabl-system-config in a deployed environment makes vrouter
        # linklocal metadata to go missing.
        # vrouter-agent will stuck in Init state with "No configuration for
        # self" error.
        global_vrouter_config_uuid = \
            self._create_global_vrouter_config()['uuid']
        with self.override_role():
            self.router_client.show_global_vrouter_config(
                global_vrouter_config_uuid)

    @decorators.skip_because(bug="1792446")
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_global_vrouter_config"])
    @decorators.idempotent_id('36fcdd51-c42b-4e67-8c26-73d4cde47507')
    def test_update_global_vrouter_config(self):
        """test method for update global vrouter config objects"""
        # This test may make your environment unstable
        # Juniper JTAC 2018-0912-0503
        #
        # Creating a global-vrouter-config object with parent as
        # default-gloabl-system-config in a deployed environment makes vrouter
        # linklocal metadata to go missing.
        # vrouter-agent will stuck in Init state with "No configuration for
        # self" error.
        updated_fq_name = data_utils.rand_name(
            'rbac-global-vrouter-config-new-name')
        global_vrouter_config_uuid = \
            self._create_global_vrouter_config()['uuid']
        with self.override_role():
            self.router_client.update_global_vrouter_config(
                global_vrouter_config_uuid,
                display_name=updated_fq_name)

    @decorators.skip_because(bug="1792446")
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_global_vrouter_config"])
    @decorators.idempotent_id('4f3d59e8-3dac-4346-9d13-5ebe5ad8f6cf')
    def test_delete_global_vrouter_config(self):
        """test method for delete global vrouter config objects"""
        if CONF.sdn.test_vrouter_global_config:
            raise self.skipException('Vrouter global config tests are '
                                     'disabled. Enabling may make your '
                                     'environment unstable.')

        global_vrouter_config_uuid = \
            self._create_global_vrouter_config()['uuid']
        with self.override_role():
            self.router_client.delete_global_vrouter_config(
                global_vrouter_config_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_logical_routers"])
    @decorators.idempotent_id('674bf3de-a9e5-45c2-921b-b89db73a2abe')
    def test_list_logical_routers(self):
        """test method for list logical router objects"""
        with self.override_role():
            self.router_client.list_logical_routers()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_logical_routers"])
    @decorators.idempotent_id('610f051b-8eba-4d3a-ba43-91386bfc0e52')
    def test_create_logical_routers(self):
        """test method for create logical router objects"""
        with self.override_role():
            self._create_logical_router()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_logical_router"])
    @decorators.idempotent_id('992841d4-0d5d-4d85-b513-049b33e2a2e2')
    def test_show_logical_router(self):
        """test method for show logical router objects"""
        logical_router_uuid = self._create_logical_router()['uuid']
        with self.override_role():
            self.router_client.show_logical_router(logical_router_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_logical_router"])
    @decorators.idempotent_id('518197bf-5233-4059-9021-5d7ecc74718e')
    def test_update_logical_router(self):
        """test method for update logical router objects"""
        updated_fq_name = data_utils.rand_name('rbac-logical-router-new-name')
        logical_router_uuid = self._create_logical_router()['uuid']
        with self.override_role():
            self.router_client.update_logical_router(
                logical_router_uuid,
                display_name=updated_fq_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_logical_router"])
    @decorators.idempotent_id('70448b9c-4444-45e0-b307-7bff4dc075b1')
    def test_delete_logical_router(self):
        """test method for delete logical router objects"""
        logical_router_uuid = self._create_logical_router()['uuid']
        with self.override_role():
            self.router_client.delete_logical_router(logical_router_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_virtual_routers"])
    @decorators.idempotent_id('604dc476-732e-4890-8665-a497360f5475')
    def test_list_virtual_routers(self):
        """test method for list virtual router objects"""
        with self.override_role():
            self.router_client.list_virtual_routers()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_virtual_routers"])
    @decorators.idempotent_id('114beb14-45c0-4714-a407-d160bb102022')
    def test_create_virtual_routers(self):
        """test method for create virtual router objects"""
        with self.override_role():
            self._create_virtual_router()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_virtual_router"])
    @decorators.idempotent_id('258fe4e0-3e39-460f-aafa-e3b53c96e534')
    def test_show_virtual_router(self):
        """test method for show virtual router objects"""
        virtual_router_uuid = self._create_virtual_router()['uuid']
        with self.override_role():
            self.router_client.show_virtual_router(virtual_router_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_virtual_router"])
    @decorators.idempotent_id('d1c72191-2068-4552-a78f-038cdd4c9c1d')
    def test_update_virtual_router(self):
        """test method for update virtual router objects"""
        updated_fq_name = data_utils.rand_name('rbac-virtual-router-new-name')
        virtual_router_uuid = self._create_virtual_router()['uuid']
        with self.override_role():
            self.router_client.update_virtual_router(
                virtual_router_uuid,
                display_name=updated_fq_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_virtual_router"])
    @decorators.idempotent_id('efbe25d6-8763-42d4-baf6-9f342e710144')
    def test_delete_virtual_router(self):
        """test method for delete virtual router objects"""
        virtual_router_uuid = self._create_virtual_router()['uuid']
        with self.override_role():
            self.router_client.delete_virtual_router(virtual_router_uuid)
