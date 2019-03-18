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
Tempest test-case to test interfaces objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class InterfacesTest(rbac_base.BaseContrailTest):
    """Test class to test interfaces objects using RBAC roles"""

    router_name = data_utils.rand_name('rbac-physical-router')
    physical_if_name = data_utils.rand_name('rbac-physical-interface')
    logical_if_name = data_utils.rand_name('rbac-logical-interface')

    def _create_physical_router(self):
        fq_name = ['default-global-system-config', self.router_name]
        post_body = {'parent_type': 'global-system-config'}
        post_body['fq_name'] = fq_name

        router = self.router_client.create_physical_routers(
            **post_body)['physical-router']
        self.addCleanup(self._try_delete_resource,
                        self.router_client.delete_physical_router,
                        router['uuid'])
        return router

    def _create_physical_interface(self):
        fq_name = ['default-global-system-config', self.router_name,
                   self.physical_if_name]
        post_body = {'parent_type': 'physical-router'}
        post_body['fq_name'] = fq_name

        physical_if = self.interface_client.create_physical_interfaces(
            **post_body)['physical-interface']
        self.addCleanup(self._try_delete_resource,
                        self.interface_client.delete_physical_interface,
                        physical_if['uuid'])
        return physical_if

    def _create_logical_interface(self):
        fq_name = ['default-global-system-config', self.router_name,
                   self.physical_if_name, self.logical_if_name]
        post_body = {'parent_type': 'physical-interface'}
        post_body['fq_name'] = fq_name

        logical_if = self.interface_client.create_logical_interfaces(
            **post_body)['logical-interface']
        self.addCleanup(self._try_delete_resource,
                        self.interface_client.delete_logical_interface,
                        logical_if['uuid'])
        return logical_if

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_physical_interfaces"])
    @decorators.idempotent_id('c496a2b4-51b2-4674-a60e-483a315baccb')
    def test_list_physical_interfaces(self):
        """test method for list physical interfaces objects"""
        with self.override_role():
            self.interface_client.list_physical_interfaces()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_physical_interfaces"])
    @decorators.idempotent_id('066f53d8-3d2a-4ad6-983f-243de7c12962')
    def test_create_physical_interfaces(self):
        """test method for create physical interfaces objects"""
        self._create_physical_router()
        with self.override_role():
            self._create_physical_interface()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_physical_interface"])
    @decorators.idempotent_id('91c4fc90-ed0f-42ec-87c6-ff6c2a9ab8de')
    def test_update_physical_interface(self):
        """test method for update physical interfaces objects"""
        self._create_physical_router()
        uuid = self._create_physical_interface()['uuid']
        # Required for Contrail 3.0.3 but not for 3.1.1
        response = self.interface_client.show_physical_interface(uuid)
        body = response['physical-interface']
        owner = body['perms2']['owner']
        with self.override_role():
            change_access = {"owner": owner, "owner_access": 6, "share": [],
                             "global_access": 0}
            body = {"perms2": change_access}
            self.interface_client.update_physical_interface(
                uuid, **body)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_physical_interface"])
    @decorators.idempotent_id('5d77ea76-be8c-49cc-8f08-72fbdaf9028f')
    def test_delete_physical_interface(self):
        """test method for delete physical interfaces objects"""
        self._create_physical_router()
        uuid = self._create_physical_interface()['uuid']
        with self.override_role():
            self.interface_client.delete_physical_interface(uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_physical_interface"])
    @decorators.idempotent_id('2c75c7e7-ef34-4e24-9c2f-5a2182db33a6')
    def test_show_physical_interface(self):
        """test method for show physical interfaces objects"""
        self._create_physical_router()
        uuid = self._create_physical_interface()['uuid']
        with self.override_role():
            self.interface_client.show_physical_interface(uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_logical_interfaces"])
    @decorators.idempotent_id('43ac3727-4a43-42d7-b52f-df75018915b9')
    def test_list_logical_interfaces(self):
        """test method for list physical interfaces objects"""
        with self.override_role():
            self.interface_client.list_logical_interfaces()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_logical_interfaces"])
    @decorators.idempotent_id('503facf2-0752-47e4-a0a4-7a3103133a61')
    def test_create_logical_interfaces(self):
        """test method for create logical interfaces objects"""
        self._create_physical_router()
        self._create_physical_interface()
        with self.override_role():
            self._create_logical_interface()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_logical_interface"])
    @decorators.idempotent_id('63c991f4-6aba-454c-9c49-522dc77b3f5c')
    def test_update_logical_interface(self):
        """test method for update logical interfaces objects"""
        self._create_physical_router()
        self._create_physical_interface()
        uuid = self._create_logical_interface()['uuid']
        # Required for Contrail 3.0.3 but not for 3.1.1
        response = self.interface_client.show_logical_interface(uuid)
        body = response['logical-interface']
        owner = body['perms2']['owner']
        with self.override_role():
            change_access = {"owner": owner, "owner_access": 6, "share": [],
                             "global_access": 0}
            body = {"perms2": change_access}
            self.interface_client.update_logical_interface(
                uuid, **body)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_logical_interface"])
    @decorators.idempotent_id('a36743d1-3ea1-4cf5-89d8-9c0b885fa625')
    def test_delete_logical_interface(self):
        """test method for update logical interfaces objects"""
        self._create_physical_router()
        self._create_physical_interface()
        uuid = self._create_logical_interface()['uuid']
        with self.override_role():
            self.interface_client.delete_logical_interface(uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_logical_interface"])
    @decorators.idempotent_id('f0f7fab7-eeb9-4d29-8415-31a50180fb44')
    def test_show_logical_interface(self):
        """test method for show logical interfaces objects"""
        self._create_physical_router()
        self._create_physical_interface()
        uuid = self._create_logical_interface()['uuid']
        with self.override_role():
            self.interface_client.show_logical_interface(uuid)
