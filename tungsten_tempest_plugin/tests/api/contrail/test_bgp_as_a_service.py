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
Tempest test-case to test BGP as a Service objects using RBAC roles
"""

from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF


class BGPAsAServicesTest(rbac_base.BaseContrailTest):
    """Test class to test BGP as a Service objects using RBAC roles"""

    def _create_bgp_as_a_services(self):
        bgp_name = data_utils.rand_name('test-bgp')
        bgp_fq_name = ['default-domain', self.tenant_name, bgp_name]
        new_bgp = self.bgp_as_a_service_client.create_bgp_as_a_services(
            parent_type='project',
            fq_name=bgp_fq_name)['bgp-as-a-service']
        self.addCleanup(self._try_delete_resource,
                        self.bgp_as_a_service_client.delete_bgp_as_a_service,
                        new_bgp['uuid'])
        return new_bgp

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_bgp_as_a_services"])
    @decorators.idempotent_id('d3153cd0-379e-4e62-9780-ef237e567fc5')
    def test_list_bgp_as_a_services(self):
        """test method for list bgp as a service objects"""
        with self.override_role():
            self.bgp_as_a_service_client.list_bgp_as_a_services()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_bgp_as_a_services"])
    @decorators.idempotent_id('a039f0c4-b53a-492b-a5c5-fbdf046afcf4')
    def test_create_bgp_as_a_services(self):
        """test method for create bgp as a service objects"""
        with self.override_role():
            self._create_bgp_as_a_services()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_bgp_as_a_service"])
    @decorators.idempotent_id('c2fae8b4-929c-4d2f-914d-76a7414a56dc')
    def test_show_bgp_as_a_service(self):
        """test method for show bgp as a service objects"""
        new_bgp = self._create_bgp_as_a_services()
        with self.override_role():
            self.bgp_as_a_service_client.show_bgp_as_a_service(
                new_bgp['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_bgp_as_a_service"])
    @decorators.idempotent_id('78c8389a-7bb5-4027-bae1-923af3d6e77c')
    def test_delete_bgp_as_a_service(self):
        """test method for delete bgp as a service objects"""
        new_bgp = self._create_bgp_as_a_services()
        with self.override_role():
            self.bgp_as_a_service_client.delete_bgp_as_a_service(
                new_bgp['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_bgp_as_a_service"])
    @decorators.idempotent_id('38ba2ecb-71e2-4a2f-be43-e82491dffa05')
    def test_update_bgp_as_a_service(self):
        """test method for update bgp as a service objects"""
        new_bgp = self._create_bgp_as_a_services()
        with self.override_role():
            self.bgp_as_a_service_client.update_bgp_as_a_service(
                new_bgp['uuid'],
                display_name=data_utils.rand_name('test-bgp'))
