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
Tempest test-case to test namespace objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class NamespaceContrailTest(rbac_base.BaseContrailTest):
    """Test class to test namespace objects using RBAC roles"""

    def _create_namespace(self):
        fq_name = data_utils.rand_name('namespace')
        post_body = {
            'parent_type': 'domain',
            'fq_name': ['default-domain', fq_name]
        }
        resp_body = self.namespace_client.create_namespaces(**post_body)
        namespace_uuid = resp_body['namespace']['uuid']
        self.addCleanup(self._try_delete_resource,
                        self.namespace_client.delete_namespace,
                        namespace_uuid)
        return namespace_uuid

    def _update_namespace(self, namespace_uuid):
        put_body = {
            'display_name': data_utils.rand_name('namespace')
        }
        self.namespace_client.update_namespace(namespace_uuid, **put_body)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_namespaces"])
    @decorators.idempotent_id('e436390d-d669-4047-9838-421ea93e94be')
    def test_list_namespaces(self):
        """test method for list namespace objects"""
        with self.override_role():
            self.namespace_client.list_namespaces()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_namespaces"])
    @decorators.idempotent_id('503ae445-7e67-4db6-989a-af0b7f9a7e95')
    def test_create_namespaces(self):
        """test method for create namespace objects"""
        with self.override_role():
            self._create_namespace()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_namespace"])
    @decorators.idempotent_id('f916971a-7c07-4386-b887-8b78d8a1e528')
    def test_show_namespace(self):
        """test method for show namespace objects"""
        namespace_uuid = self._create_namespace()
        with self.override_role():
            self.namespace_client.show_namespace(namespace_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_namespace"])
    @decorators.idempotent_id('3649f65a-922a-4b8a-9b8b-520c333e192e')
    def test_update_namespace(self):
        """test method for update namespace objects"""
        namespace_uuid = self._create_namespace()
        with self.override_role():
            self._update_namespace(namespace_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_namespace"])
    @decorators.idempotent_id('80e736bf-fc7d-4274-8173-a50c883776a9')
    def test_delete_namespace(self):
        """test method for delete namespace objects"""
        namespace_uuid = self._create_namespace()
        with self.override_role():
            self.namespace_client.delete_namespace(namespace_uuid)
