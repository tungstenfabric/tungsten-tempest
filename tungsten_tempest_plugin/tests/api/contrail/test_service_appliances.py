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

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

from patrole_tempest_plugin import rbac_rule_validation

from tempest import config
from tempest.lib import decorators
from tempest.lib.common.utils import data_utils
from tempest.lib.decorators import idempotent_id

CONF = config.CONF


class ServiceAppliancesTest(rbac_base.BaseContrailTest):

    """
    Test class to test service appliances objects using RBAC roles
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

    def _create_service_appliance_sets(self, global_system_config):
        set_name = data_utils.rand_name('test-set')
        set_fq_name = [global_system_config, set_name]
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

    @decorators.idempotent_id('6376afa3-7917-4396-8aff-d821592b4f2c')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_service_appliances")
    @idempotent_id('6b5fc17c-34e6-4d21-a53e-a0dfe69afd31')
    def test_list_service_appliances(self):
        """
        test method for list service appliance objects
        """
        with self.rbac_utils.override_role(self):
            self.service_appliances_client.list_service_appliances()

    @decorators.idempotent_id('a9f1ccc9-b1fd-4ace-96ae-43c3912f0cfc')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_service_appliances")
    @idempotent_id('0563c0c8-b986-466e-8540-aa8ad7a10367')
    def test_create_service_appliances(self):
        """
        test method for create service appliance objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        new_set = \
            self._create_service_appliance_sets(global_system_config)
        with self.rbac_utils.override_role(self):
            self._create_service_appliances(new_set)

    @decorators.idempotent_id('247d0ed3-3cdc-4878-b637-80b8f65eb3a1')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_service_appliance")
    @idempotent_id('ea30dcfe-8657-4a7d-9cf1-3176d334bf27')
    def test_show_service_appliance(self):
        """
        test method for show service appliance objects
        """
        # Create global system config
        global_system_config = \
            self._create_global_system_config()['name']
        new_set = \
            self._create_service_appliance_sets(global_system_config)
        new_appliance = self._create_service_appliances(new_set)
        with self.rbac_utils.override_role(self):
            self.service_appliances_client.show_service_appliance(
                new_appliance['uuid'])

    @decorators.idempotent_id('142fd7b3-f79c-46a8-b60f-51a3380a9f3b')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_service_appliance")
    @idempotent_id('a54ca33a-8590-4844-96d7-b96882b59e86')
    def test_update_service_appliance(self):
        """
        test method for update service appliance objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        new_set = \
            self._create_service_appliance_sets(global_system_config)
        new_appliance = self._create_service_appliances(new_set)
        update_name = data_utils.rand_name('test')
        with self.rbac_utils.override_role(self):
            self.service_appliances_client.update_service_appliance(
                new_appliance['uuid'],
                display_name=update_name)

    @decorators.idempotent_id('2e9d6bb8-e616-445b-b87b-1e7e7f5387b7')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_service_appliance")
    @idempotent_id('362deff5-7b72-4929-ba81-972cfcfa1309')
    def test_delete_service_appliance(self):
        """
        test method for delete service appliance objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        new_set = \
            self._create_service_appliance_sets(global_system_config)
        new_appliance = self._create_service_appliances(new_set)
        with self.rbac_utils.override_role(self):
            self.service_appliances_client.delete_service_appliance(
                new_appliance['uuid'])

    @decorators.idempotent_id('4fec3bd7-1c7b-46ba-8b29-228a6dc35592')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_service_appliance_sets")
    @idempotent_id('c1e74da9-00b6-4c88-adda-2ce49094e570')
    def test_list_service_appl_sets(self):
        """
        test method for list service appliance sets objects
        """
        with self.rbac_utils.override_role(self):
            self.service_appliances_client.list_service_appliance_sets()

    @decorators.idempotent_id('c0647738-11fd-4c73-846b-1d54aff2eef8')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_service_appliance_sets")
    @idempotent_id('eb00d6cf-590f-41bf-8ee4-5be625d9cb93')
    def test_create_service_appl_sets(self):
        """
        test method for create service appliance sets objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        with self.rbac_utils.override_role(self):
            self._create_service_appliance_sets(global_system_config)

    @decorators.idempotent_id('f27d4f96-9db6-4a97-8dbf-75ba14c08ae3')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_service_appliance_set")
    @idempotent_id('dd35dd04-e7d9-46bb-8f36-26835f122572')
    def test_show_service_appl_set(self):
        """
        test method for show service appliance sets objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        new_set = self._create_service_appliance_sets(
            global_system_config)
        with self.rbac_utils.override_role(self):
            self.service_appliances_client.show_service_appliance_set(
                new_set['uuid'])

    @decorators.idempotent_id('64ad1226-bbd5-4322-8534-e3eb98413e6c')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_service_appliance_set")
    @idempotent_id('952f063b-bc71-4f62-83b1-719bce5ad4ed')
    def test_update_service_appl_set(self):
        """
        test method for update service appliance sets objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        new_set = self._create_service_appliance_sets(
            global_system_config)
        update_name = data_utils.rand_name('test')
        with self.rbac_utils.override_role(self):
            self.service_appliances_client.update_service_appliance_set(
                new_set['uuid'],
                display_name=update_name)

    @decorators.idempotent_id('6bbd4831-76cf-492e-9908-7405f694889b')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_service_appliance_set")
    @idempotent_id('7b56ce24-da1d-4565-bd22-c58dc57d7045')
    def test_delete_service_appl_set(self):
        """
        test method for delete service appliance sets objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        new_set = self._create_service_appliance_sets(
            global_system_config)
        with self.rbac_utils.override_role(self):
            self.service_appliances_client.delete_service_appliance_set(
                new_set['uuid'])
