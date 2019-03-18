# Copyright 2018 AT&T Corp
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

from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF


class FabricContrailTest(rbac_base.BaseContrailTest):

    required_contrail_version = 5

    @classmethod
    def resource_setup(cls):
        super(FabricContrailTest, cls).resource_setup()
        cls.fabric_uuid = cls._create_fabric()

    @classmethod
    def _create_fabric(cls):
        fabric = cls.contrail_client.create_fabric(
            fq_name=["default-global-system-config",
                     data_utils.rand_name('fabric')],
            parent_type="global-system-config")
        cls.addClassResourceCleanup(cls._try_delete_resource,
                                    cls.contrail_client.delete_fabric,
                                    fabric["fabric"]["uuid"])
        return fabric["fabric"]["uuid"]

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_fabrics"])
    @decorators.idempotent_id('9005d1d6-3bd2-4378-b145-0fda130ce1d1')
    def test_list_fabric_s(self):
        """List fabrics

        RBAC test for the Contrail list_fabrics policy
        """
        with self.override_role():
            self.contrail_client.list_fabrics()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_fabric"])
    @decorators.idempotent_id('9b216ca5-b332-41ca-9072-6c3ee325ea91')
    def test_create_fabric(self):
        """Create fabric

        RBAC test for the Contrail create_fabric policy
        """
        with self.override_role():
            self._create_fabric()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_fabric"])
    @decorators.idempotent_id('244c3530-70e0-4efe-98be-4c2d1ffa0376')
    def test_show_fabric(self):
        """Show fabric

        RBAC test for the Contrail show_fabric policy
        """
        with self.override_role():
            self.contrail_client.show_fabric(self.fabric_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_fabric"])
    @decorators.idempotent_id('75edc6b9-c66a-46fc-a271-4c54e4cc77b1')
    def test_delete_fabric(self):
        """Delete fabric

        RBAC test for the Contrail delete_fabric policy
        """
        fab_uuid = self._create_fabric()
        with self.override_role():
            self.contrail_client.delete_fabric(fab_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_fabric"])
    @decorators.idempotent_id('f22c4c26-3843-4fc6-a8ff-7890d5ad1c39')
    def test_update_fabric(self):
        """Update fabric

        RBAC test for the Contrail update_fabric policy
        """
        with self.override_role():
            put_body = {'display_name': data_utils.rand_name('update_fab')}
            self.contrail_client.update_fabric(self.fabric_uuid, **put_body)
