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


class FabricNamespacesContrailTest(rbac_base.BaseContrailTest):

    required_contrail_version = 5

    @classmethod
    def resource_setup(cls):
        super(FabricNamespacesContrailTest, cls).resource_setup()
        cls.fabric_namespace_uuid = cls._create_fabric_namespace()

    @classmethod
    def _create_fabric(cls):
        # Fabric object is required as parent for fabric-namespace
        fabric = cls.contrail_client.create_fabric(
            fq_name=["default-global-system-config",
                     data_utils.rand_name('fabric')],
            parent_type="global-system-config")
        cls.addClassResourceCleanup(cls._try_delete_resource,
                                    cls.contrail_client.delete_fabric,
                                    fabric["fabric"]["uuid"])
        return fabric["fabric"]

    @classmethod
    def _create_fabric_namespace(cls):
        fabric = cls._create_fabric()

        parent_type = 'fabric'
        name = data_utils.rand_name('fabric_namespace')
        fq_name = fabric["fq_name"] + [name]

        post_body = {
            'fq_name': fq_name,
            'parent_type': parent_type
        }

        resp_body = cls.contrail_client.create_fabric_namespace(**post_body)
        cls.addClassResourceCleanup(
            cls._try_delete_resource,
            cls.contrail_client.delete_fabric_namespace,
            resp_body['fabric-namespace']['uuid'])

        return resp_body['fabric-namespace']['uuid']

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_fabric_namespaces"])
    @decorators.idempotent_id('f9935e2a-c4b6-4694-8698-6148faf93e1a')
    def test_list_fabric_namespaces(self):
        """List fabric namespaces

        RBAC test for the Contrail list_fabric_namespaces policy
        """
        with self.override_role():
            self.contrail_client.list_fabric_namespaces()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_fabric_namespace"])
    @decorators.idempotent_id('5bb85072-130d-4f36-a787-12b65bdd4c03')
    def test_create_fabric_namespace(self):
        """Create fabric namespace

        RBAC test for the Contrail create_fabric_namespace policy
        """
        with self.override_role():
            self._create_fabric_namespace()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_fabric_namespace"])
    @decorators.idempotent_id('5ab5bc8f-7209-427a-9868-4fbc7a7e0d85')
    def test_show_fabric_namespace(self):
        """Show fabric namespace

        RBAC test for the Contrail show_fabric_namespace policy
        """
        with self.override_role():
            self.contrail_client.show_fabric_namespace(
                self.fabric_namespace_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_fabric_namespace"])
    @decorators.idempotent_id('ff20e4bb-6110-476e-80b4-d6114981e8bf')
    def test_delete_fabric_namespace(self):
        """Delete fabric namespace

        RBAC test for the Contrail delete_fabric_namespace policy
        """
        ns_uuid = self._create_fabric_namespace()
        with self.override_role():
            self.contrail_client.delete_fabric_namespace(ns_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_fabric_namespace"])
    @decorators.idempotent_id('78514d86-fcdc-4bc6-99b9-11b5e91b5296')
    def test_update_fabric_namespace(self):
        """Update fabric namespace

        RBAC test for the Contrail update_fabric_namespace policy
        """
        with self.override_role():
            put_body = {'display_name': data_utils.rand_name('update_fns')}
            self.contrail_client.update_fabric_namespace(
                self.fabric_namespace_uuid, **put_body)
