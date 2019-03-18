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
Tempest test-case to test service appliance using RBAC roles
"""

from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF


class ServiceAppliancesTest(rbac_base.BaseContrailTest):
    """Test class to test service appliances objects using RBAC roles"""

    def _create_service_appliance_sets(self):
        set_name = data_utils.rand_name('test-set')
        set_fq_name = ['default-global-system-config', set_name]
        new_set = self.service_appliances_client.create_service_appliance_sets(
            parent_type='global-system-config',
            fq_name=set_fq_name)['service-appliance-set']
        self.addCleanup(self._try_delete_resource,
                        (self.service_appliances_client.
                         delete_service_appliance_set),
                        new_set['uuid'])
        return new_set

    def _create_service_appliances(self, app_set):
        appliance_name = data_utils.rand_name('test-appliance')
        appliance_fq_name = app_set['fq_name']
        appliance_fq_name.append(appliance_name)
        new_appliance = \
            self.service_appliances_client.create_service_appliances(
                parent_type='service-appliance-set',
                fq_name=appliance_fq_name)['service-appliance']
        self.addCleanup(self._try_delete_resource,
                        (self.service_appliances_client.
                         delete_service_appliance),
                        new_appliance['uuid'])
        return new_appliance

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_service_appliances"])
    @decorators.idempotent_id('6b5fc17c-34e6-4d21-a53e-a0dfe69afd31')
    def test_list_service_appliances(self):
        """test method for list service appliance objects"""
        with self.override_role():
            self.service_appliances_client.list_service_appliances()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_service_appliances"])
    @decorators.idempotent_id('0563c0c8-b986-466e-8540-aa8ad7a10367')
    def test_create_service_appliances(self):
        """test method for create service appliance objects"""
        new_set = self._create_service_appliance_sets()
        with self.override_role():
            self._create_service_appliances(new_set)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_service_appliance"])
    @decorators.idempotent_id('ea30dcfe-8657-4a7d-9cf1-3176d334bf27')
    def test_show_service_appliance(self):
        """test method for show service appliance objects"""
        new_set = self._create_service_appliance_sets()
        new_appliance = self._create_service_appliances(new_set)
        with self.override_role():
            self.service_appliances_client.show_service_appliance(
                new_appliance['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_service_appliance"])
    @decorators.idempotent_id('a54ca33a-8590-4844-96d7-b96882b59e86')
    def test_update_service_appliance(self):
        """test method for update service appliance objects"""
        new_set = self._create_service_appliance_sets()
        new_appliance = self._create_service_appliances(new_set)
        update_name = data_utils.rand_name('test')
        with self.override_role():
            self.service_appliances_client.update_service_appliance(
                new_appliance['uuid'],
                display_name=update_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_service_appliance"])
    @decorators.idempotent_id('362deff5-7b72-4929-ba81-972cfcfa1309')
    def test_delete_service_appliance(self):
        """test method for delete service appliance objects"""
        new_set = self._create_service_appliance_sets()
        new_appliance = self._create_service_appliances(new_set)
        with self.override_role():
            self.service_appliances_client.delete_service_appliance(
                new_appliance['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_service_appliance_sets"])
    @decorators.idempotent_id('c1e74da9-00b6-4c88-adda-2ce49094e570')
    def test_list_service_appl_sets(self):
        """test method for list service appliance sets objects"""
        with self.override_role():
            self.service_appliances_client.list_service_appliance_sets()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_service_appliance_sets"])
    @decorators.idempotent_id('eb00d6cf-590f-41bf-8ee4-5be625d9cb93')
    def test_create_service_appl_sets(self):
        """test method for create service appliance sets objects"""
        with self.override_role():
            self._create_service_appliance_sets()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_service_appliance_set"])
    @decorators.idempotent_id('dd35dd04-e7d9-46bb-8f36-26835f122572')
    def test_show_service_appl_set(self):
        """test method for show service appliance sets objects"""
        new_set = self._create_service_appliance_sets()
        with self.override_role():
            self.service_appliances_client.show_service_appliance_set(
                new_set['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_service_appliance_set"])
    @decorators.idempotent_id('952f063b-bc71-4f62-83b1-719bce5ad4ed')
    def test_update_service_appl_set(self):
        """test method for update service appliance sets objects"""
        new_set = self._create_service_appliance_sets()
        update_name = data_utils.rand_name('test')
        with self.override_role():
            self.service_appliances_client.update_service_appliance_set(
                new_set['uuid'],
                display_name=update_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_service_appliance_set"])
    @decorators.idempotent_id('7b56ce24-da1d-4565-bd22-c58dc57d7045')
    def test_delete_service_appl_set(self):
        """test method for delete service appliance sets objects"""
        new_set = self._create_service_appliance_sets()
        with self.override_role():
            self.service_appliances_client.delete_service_appliance_set(
                new_set['uuid'])
