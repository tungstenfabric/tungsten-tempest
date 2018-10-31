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
Tempest test-case to test database objects using RBAC roles
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


class ContrailDatabaseTest(rbac_base.BaseContrailTest):

    """
    Test class to test database objects using RBAC roles
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

    def _delete_database_node(self, db_node_id):
        return self.db_client.delete_database_node(db_node_id)

    def _create_database_node(self, global_system_config):
        name = data_utils.rand_name('database')
        fq_name = [global_system_config, name]
        database_node_ip_address = '1.1.1.1'
        parent_type = 'global-system-config'
        db_node = self.db_client.create_databse_nodes(
            display_name=name,
            database_node_ip_address=database_node_ip_address,
            fq_name=fq_name,
            parent_type=parent_type)['database-node']

        self.addCleanup(self._try_delete_resource,
                        self._delete_database_node,
                        db_node['uuid'])
        return db_node

    @decorators.idempotent_id('fbf74117-4fdb-4b95-9469-a71b708afd47')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_database_nodes")
    @idempotent_id('5ae6f965-6161-443f-b19e-dfa7b364c533')
    def test_list_database_nodes(self):
        """
        test method for list database objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        self._create_database_node(global_system_config)
        with self.rbac_utils.override_role(self):
            self.db_client.list_database_nodes()

    @decorators.idempotent_id('6749a9db-54ff-448d-a590-5050a4db7946')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_database_node")
    @idempotent_id('4a07d9a8-7b99-43bd-b628-06c023993aab')
    def test_show_database_node(self):
        """
        test method for show database objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        db_node = self._create_database_node(global_system_config)
        db_node_id = db_node['uuid']
        with self.rbac_utils.override_role(self):
            self.db_client.show_database_node(db_node_id)

    @decorators.idempotent_id('672bb09f-e31b-4492-9858-a190d701949f')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_database_nodes")
    @idempotent_id('b9aa9c6b-9381-44f0-94fb-e4523bf2a87e')
    def test_create_database_nodes(self):
        """
        test method for update database objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        with self.rbac_utils.override_role(self):
            self._create_database_node(global_system_config)

    @decorators.idempotent_id('f959251d-e925-4f98-a297-3bcde77fbf0d')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_database_node")
    @idempotent_id('6e59f393-0e55-4327-871e-7f0ad53f2e17')
    def test_update_database_node(self):
        """
        test method for update database objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        db_node = self._create_database_node(global_system_config)
        db_node_id = db_node['uuid']
        display_name = data_utils.rand_name('DatabaseNew')
        with self.rbac_utils.override_role(self):
            self.db_client.update_database_node(
                db_node_id=db_node_id,
                display_name=display_name)

    @decorators.idempotent_id('d6981e37-3b04-4883-8411-12fc69d2aa98')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_database_node")
    @idempotent_id('0cbc5a52-d7e7-4a1c-a85d-6bf44012d99b')
    def test_delete_database_node(self):
        """
        test method for delete database objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        db_node = self._create_database_node(global_system_config)
        db_node_id = db_node['uuid']
        with self.rbac_utils.override_role(self):
            self._delete_database_node(db_node_id)
