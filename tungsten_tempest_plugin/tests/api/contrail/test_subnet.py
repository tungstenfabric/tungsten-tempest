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
Tempest test-case to test subnet objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class SubnetContrailTest(rbac_base.BaseContrailTest):
    """Test class to test subnet objects using RBAC roles"""

    def _create_subnet(self):
        post_body = {
            'fq_name': [data_utils.rand_name('subnet')]
        }
        resp_body = self.subnet_client.create_subnets(
            **post_body)
        subnet_uuid = resp_body['subnet']['uuid']
        self.addCleanup(self._try_delete_resource,
                        self.subnet_client.delete_subnet,
                        subnet_uuid)
        return subnet_uuid

    def _update_subnet(self, subnet_uuid):
        put_body = {
            'display_name': data_utils.rand_name('subnet')
        }
        self.subnet_client.update_subnet(subnet_uuid, **put_body)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_subnets"])
    @decorators.idempotent_id('ddd1d9ae-cf2f-4a74-98ba-b0f481f27977')
    def test_list_subnets(self):
        """test method for list subnet objects"""
        with self.override_role():
            self.subnet_client.list_subnets()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_subnets"])
    @decorators.idempotent_id('ee0cb904-d162-44a4-b7b0-a7451f667ed5')
    def test_create_subnets(self):
        """test method for create subnet objects"""
        with self.override_role():
            self._create_subnet()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_subnet"])
    @decorators.idempotent_id('994618f2-5b40-460c-a6a8-6479bc15bf80')
    def test_show_subnet(self):
        """test method for show subnet objects"""
        subnet_uuid = self._create_subnet()
        with self.override_role():
            self.subnet_client.show_subnet(subnet_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_subnet"])
    @decorators.idempotent_id('565e44c9-eb9b-4ae6-9ebb-db422a9751ee')
    def test_update_subnet(self):
        """test method for update subnet objects"""
        subnet_uuid = self._create_subnet()
        with self.override_role():
            self._update_subnet(subnet_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_subnet"])
    @decorators.idempotent_id('a733b913-7a88-45d9-ac0a-d858fa3dc662')
    def test_delete_subnet(self):
        """test method for delete subnet objects"""
        subnet_uuid = self._create_subnet()
        with self.override_role():
            self.subnet_client.delete_subnet(subnet_uuid)
