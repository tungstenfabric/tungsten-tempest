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
Tempest test-case to test dsa rules objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class ContrailDSARuleTest(rbac_base.BaseContrailTest):
    """Test class to test DSA rule objects using RBAC roles"""

    def _create_discovery_service_assignments(self):
        dsa_name = [data_utils.rand_name('test-dsa')]
        new_dsa = self.dsa_client.create_ds_assignments(
            fq_name=dsa_name)['discovery-service-assignment']

        self.addCleanup(self._try_delete_resource,
                        self.dsa_client.delete_ds_assignment,
                        new_dsa['uuid'])
        return new_dsa

    def _create_dsa_rules(self, discovery_service_assignment):
        rule_name = data_utils.rand_name('dsa-rule')
        post_data = {
            'fq_name': [discovery_service_assignment, rule_name],
            'parent_type': 'discovery-service-assignment'
        }
        new_rule = self.dsa_rule_client.create_dsa_rules(
            **post_data)['dsa-rule']
        self.addCleanup(self._try_delete_resource,
                        self.dsa_rule_client.delete_dsa_rule,
                        new_rule['uuid'])
        return new_rule

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_dsa_rules"])
    @decorators.idempotent_id('3227673b-96fc-4d26-ab0b-109347e9e9c2')
    def test_list_dsa_rules(self):
        """test method for list dsa rules objects"""
        with self.override_role():
            self.dsa_rule_client.list_dsa_rules()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_dsa_rule"])
    @decorators.idempotent_id('0f90ea4f-c050-4c31-93a7-1e0c58df914e')
    def test_show_dsa_rule(self):
        """test method for show dsa rules objects"""
        # create discover service assignment
        discovery_service_assignment = \
            self._create_discovery_service_assignments()['name']
        new_rule = self._create_dsa_rules(discovery_service_assignment)
        with self.override_role():
            self.dsa_rule_client.show_dsa_rule(new_rule['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_dsa_rules"])
    @decorators.idempotent_id('c3774ca3-45d0-4ca8-a6b3-f895441b1d0e')
    def test_create_dsa_rules(self):
        """test method for create dsa rules objects"""
        # create discover service assignment
        discovery_service_assignment = \
            self._create_discovery_service_assignments()['name']
        with self.override_role():
            self._create_dsa_rules(discovery_service_assignment)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_dsa_rule"])
    @decorators.idempotent_id('5cfe7e8e-d91c-4183-8e6c-733e826707be')
    def test_update_dsa_rule(self):
        """test method for update dsa rules objects"""
        # create discover service assignment
        discovery_service_assignment = \
            self._create_discovery_service_assignments()['name']
        new_rule = self._create_dsa_rules(discovery_service_assignment)
        update_name = data_utils.rand_name('updated_rule')
        with self.override_role():
            self.dsa_rule_client.update_dsa_rule(
                new_rule['uuid'], display_name=update_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_dsa_rule"])
    @decorators.idempotent_id('d3b869db-fa49-48f0-861a-08efd9879b15')
    def test_delete_dsa_rule(self):
        """test method for delete dsa rules objects"""
        # create discover service assignment
        discovery_service_assignment = \
            self._create_discovery_service_assignments()['name']
        new_rule = self._create_dsa_rules(discovery_service_assignment)
        with self.override_role():
            self.dsa_rule_client.delete_dsa_rule(new_rule['uuid'])
