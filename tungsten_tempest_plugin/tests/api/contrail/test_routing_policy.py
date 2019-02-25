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
Tempest test-case to test routing policy objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class RoutingPolicyTest(rbac_base.BaseContrailTest):
    """Test class to test routing policy objects using RBAC roles"""

    def _create_routing_policy(self):
        fq_name = data_utils.rand_name('routing-policy')
        post_body = {
            'parent_type': 'project',
            'fq_name': ["default-domain", self.tenant_name, fq_name]
        }
        resp_body = self.routing_policy_client.create_routing_policys(
            **post_body)
        routing_policy_uuid = resp_body['routing-policy']['uuid']
        self.addCleanup(self._try_delete_resource,
                        self.routing_policy_client.delete_routing_policy,
                        routing_policy_uuid)
        return routing_policy_uuid

    def _update_routing_policy(self, routing_policy_uuid):
        put_body = {
            'display_name': data_utils.rand_name('routing-policy')
        }
        self.routing_policy_client.update_routing_policy(routing_policy_uuid,
                                                         **put_body)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_routing_policys"])
    @decorators.idempotent_id('fe25a306-bc4f-42b3-91ca-38df01e35345')
    def test_list_routing_policys(self):
        """test method for list routing policy objects"""
        with self.override_role():
            self.routing_policy_client.list_routing_policys()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_routing_policys"])
    @decorators.idempotent_id('f8ca5e30-8bb3-410f-8618-8fdca70bda06')
    def test_create_routing_policys(self):
        """test method for create routing policy objects"""
        with self.override_role():
            self._create_routing_policy()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_routing_policy"])
    @decorators.idempotent_id('3421e84e-3e2a-452a-9a26-b2caf00b1cbc')
    def test_show_routing_policy(self):
        """test method for show routing policy objects"""
        policy_uuid = self._create_routing_policy()
        with self.override_role():
            self.routing_policy_client.show_routing_policy(policy_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_routing_policy"])
    @decorators.idempotent_id('9fc1f44f-c8e2-4f5a-8239-e9b783f55d94')
    def test_update_routing_policy(self):
        """test method for update routing policy objects"""
        policy_uuid = self._create_routing_policy()
        with self.override_role():
            self._update_routing_policy(policy_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_routing_policy"])
    @decorators.idempotent_id('24f1cd7a-2917-4b81-a0a3-a40ed2d40c7d')
    def test_delete_routing_policy(self):
        """test method for delete routing policy objects"""
        policy_uuid = self._create_routing_policy()
        with self.override_role():
            self.routing_policy_client.delete_routing_policy(policy_uuid)
