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
Tempest test-case to test virtual ip objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class VirtualIPTest(rbac_base.BaseContrailTest):
    """Test class to test virtual ip objects using RBAC roles"""

    def _create_virtual_ip(self):
        fq_name = data_utils.rand_name('virtual_ip')
        post_body = {
            'parent_type': 'project',
            'fq_name': ["default-domain", self.tenant_name, fq_name]
        }
        resp_body = self.virtual_ip_client.create_virtual_ips(**post_body)
        virtual_ip_uuid = resp_body['virtual-ip']['uuid']
        self.addCleanup(self._try_delete_resource,
                        self.virtual_ip_client.delete_virtual_ip,
                        virtual_ip_uuid)
        return virtual_ip_uuid

    def _update_virtual_ip(self, virtual_ip_uuid):
        put_body = {
            'display_name': data_utils.rand_name('virtual_ip')
        }
        self.virtual_ip_client.update_virtual_ip(virtual_ip_uuid, **put_body)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_virtual_ips"])
    @decorators.idempotent_id('92303eee-bd96-48bc-a02c-39950bd19a21')
    def test_list_virtual_ips(self):
        """test method for list virtual ip objects"""
        with self.override_role():
            self.virtual_ip_client.list_virtual_ips()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_virtual_ips"])
    @decorators.idempotent_id('e0070888-995d-46ab-91fc-db1412eba2f7')
    def test_create_virtual_ips(self):
        """test method for create virtual ip objects"""
        with self.override_role():
            self._create_virtual_ip()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_virtual_ip"])
    @decorators.idempotent_id('2a4b3abd-c6f7-4d82-aa31-02e53d2a8fb9')
    def test_show_virtual_ip(self):
        """test method for show virtual ip objects"""
        virtual_ip_uuid = self._create_virtual_ip()
        with self.override_role():
            self.virtual_ip_client.show_virtual_ip(virtual_ip_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_virtual_ip"])
    @decorators.idempotent_id('0e975c92-62dc-4e6e-82cc-8cf37da3c5b2')
    def test_update_virtual_ip(self):
        """test method for update virtual ip objects"""
        virtual_ip_uuid = self._create_virtual_ip()
        with self.override_role():
            self._update_virtual_ip(virtual_ip_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_virtual_ip"])
    @decorators.idempotent_id('fd0b2635-36bd-4345-97b7-9c0a57372eba')
    def test_delete_virtual_ip(self):
        """test method for delete virtual ip objects"""
        virtual_ip_uuid = self._create_virtual_ip()
        with self.override_role():
            self.virtual_ip_client.delete_virtual_ip(virtual_ip_uuid)
