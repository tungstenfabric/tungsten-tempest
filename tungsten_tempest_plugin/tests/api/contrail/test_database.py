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
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class ContrailDatabaseTest(rbac_base.BaseContrailTest):
    """Test class to test database objects using RBAC roles"""

    def _delete_database_node(self, db_node_id):
        return self.db_client.delete_database_node(db_node_id)

    def _create_database_node(self):
        name = data_utils.rand_name('database')
        fq_name = ['default-global-system-config', name]
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

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_database_nodes"])
    @decorators.idempotent_id('5ae6f965-6161-443f-b19e-dfa7b364c533')
    def test_list_database_nodes(self):
        """test method for list database objects"""
        self._create_database_node()
        with self.override_role():
            self.db_client.list_database_nodes()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_database_node"])
    @decorators.idempotent_id('4a07d9a8-7b99-43bd-b628-06c023993aab')
    def test_show_database_node(self):
        """test method for show database objects"""
        db_node = self._create_database_node()
        with self.override_role():
            self.db_client.show_database_node(db_node['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_database_nodes"])
    @decorators.idempotent_id('b9aa9c6b-9381-44f0-94fb-e4523bf2a87e')
    def test_create_database_nodes(self):
        """test method for update database objects"""
        with self.override_role():
            self._create_database_node()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_database_node"])
    @decorators.idempotent_id('6e59f393-0e55-4327-871e-7f0ad53f2e17')
    def test_update_database_node(self):
        """test method for update database objects"""
        db_node = self._create_database_node()
        db_node_id = db_node['uuid']
        display_name = data_utils.rand_name('DatabaseNew')
        with self.override_role():
            self.db_client.update_database_node(
                db_node_id=db_node_id,
                display_name=display_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_database_node"])
    @decorators.idempotent_id('0cbc5a52-d7e7-4a1c-a85d-6bf44012d99b')
    def test_delete_database_node(self):
        """test method for delete database objects"""
        db_node = self._create_database_node()
        db_node_id = db_node['uuid']
        with self.override_role():
            self._delete_database_node(db_node_id)
