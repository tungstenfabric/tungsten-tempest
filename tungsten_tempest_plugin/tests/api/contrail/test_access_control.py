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
Tempest test-case to test Access Control using RBAC roles
"""

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

from patrole_tempest_plugin import rbac_rule_validation

from tempest import config
from tempest.lib import decorators
from tempest.lib.common.utils import data_utils
from tempest.lib.decorators import idempotent_id

CONF = config.CONF


class AccessControlTest(rbac_base.BaseContrailTest):

    """
    Test class to test Access Control objects using RBAC roles
    """

    def _create_api_access_lists(self):
        api_list_name = data_utils.rand_name('test-api-list')
        api_list_fq_name = ['default-domain', self.tenant_name, api_list_name]
        new_api_list = self.access_control_client.create_api_access_lists(
            fq_name=api_list_fq_name,
            parent_type="project")['api-access-list']

        self.addCleanup(self._try_delete_resource,
                        self.access_control_client.delete_api_access_list,
                        new_api_list['uuid'])
        return new_api_list

    def _create_security_groups(self):
        name = data_utils.rand_name('securitygroup')
        domain_name = 'default-domain'
        fq_name = ['default-domain', self.tenant_name, name]
        parent_type = 'project'
        sec_grp = self.security_group_client.create_security_groups(
            domain_name=domain_name,
            fq_name=fq_name,
            display_name=name,
            parent_type=parent_type)['security-group']
        self.addCleanup(self._try_delete_resource,
                        self._delete_security_group,
                        sec_grp['uuid'])
        return sec_grp

    def _delete_security_group(self, sec_grp_id):
        return self.security_group_client.delete_security_group(sec_grp_id)

    def _create_access_control_lists(self, sec_group_name):
        ctrl_list_name = data_utils.rand_name('test-set')
        ctrl_list_fq_name = ['default-domain', self.tenant_name,
                             sec_group_name, ctrl_list_name]
        new_ctrl_list = self.access_control_client.create_access_control_lists(
            fq_name=ctrl_list_fq_name,
            parent_type="security-group")['access-control-list']

        self.addCleanup(self._try_delete_resource,
                        self.access_control_client.delete_access_control_list,
                        new_ctrl_list['uuid'])
        return new_ctrl_list

    @decorators.idempotent_id('3fe225d4-0b50-476b-a809-caf3e485ddda')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_api_access_lists")
    @idempotent_id('2bfde8fd-36fe-4e69-ba59-6f2db8941e7d')
    def test_list_api_access_lists(self):
        """
        test method for list api access list
        """
        with self.rbac_utils.override_role(self):
            self.access_control_client.list_api_access_lists()

    @decorators.idempotent_id('e114fcdc-019e-4d94-8d25-30191fba4348')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_api_access_lists")
    @idempotent_id('b2b5f50c-07d8-4d79-b9a4-78187ad97353')
    def test_create_api_access_lists(self):
        """
        test method for create api access list
        """
        with self.rbac_utils.override_role(self):
            self._create_api_access_lists()

    @decorators.idempotent_id('4589f75d-b4fc-4ed5-a1ce-efe41a8ad879')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_api_access_list")
    @idempotent_id('b82e8e6b-83b5-424d-9652-ef6a34067f4f')
    def test_show_api_access_list(self):
        """
        test method for show api access list
        """
        new_api_list = self._create_api_access_lists()
        with self.rbac_utils.override_role(self):
            self.access_control_client.show_api_access_list(
                new_api_list['uuid'])

    @decorators.idempotent_id('54f8ceb5-183e-40c8-ba38-6c7c9298cf2f')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_api_access_list")
    @idempotent_id('edc88825-1e2e-47ff-b7b4-f68d6310fbad')
    def test_update_api_access_list(self):
        """
        test method for update api access list
        """
        new_api_list = self._create_api_access_lists()
        update_name = data_utils.rand_name('test')
        with self.rbac_utils.override_role(self):
            self.access_control_client.update_api_access_list(
                new_api_list['uuid'],
                display_name=update_name)

    @decorators.idempotent_id('1e715cbb-1250-4b4e-97c5-b4f0f5c61d60')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_api_access_list")
    @idempotent_id('f27d9044-95f2-4733-81ed-df9340dbd421')
    def test_delete_api_access_list(self):
        """
        test method for delete api access list
        """
        new_api_list = self._create_api_access_lists()
        with self.rbac_utils.override_role(self):
            self.access_control_client.delete_api_access_list(
                new_api_list['uuid'])

    @decorators.idempotent_id('e87c5239-f62a-4791-a550-ba0c7cf354f9')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_access_control_lists")
    @idempotent_id('c56a1338-a9d1-4286-8aeb-3a0d60d93037')
    def test_list_access_control_lists(self):
        """
        test method for list access control list
        """
        with self.rbac_utils.override_role(self):
            self.access_control_client.list_access_control_lists()

    @decorators.idempotent_id('c33b8b75-f03c-44e5-9986-052819134771')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_access_control_lists")
    @idempotent_id('9f225d2b-5376-42f5-97aa-cf63be47fa19')
    def test_create_access_control(self):
        """
        test method for create access control list
        """
        # Create Security Group
        sec_group = self._create_security_groups()
        with self.rbac_utils.override_role(self):
            self._create_access_control_lists(sec_group['name'])

    @decorators.idempotent_id('ab268b09-629c-4eec-b138-887be03c65b4')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_access_control_list")
    @idempotent_id('f0ed882b-f3de-48b7-884a-637ee0b7d6b6')
    def test_show_access_control_list(self):
        """
        test method for show access control list
        """
        # Create Security Group
        sec_group = self._create_security_groups()
        new_ctrl_list = self._create_access_control_lists(
            sec_group['name'])
        with self.rbac_utils.override_role(self):
            self.access_control_client.show_access_control_list(
                new_ctrl_list['uuid'])

    @decorators.idempotent_id('2811c098-198d-4a73-a635-816f4957057f')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_access_control_list")
    @idempotent_id('9a4b3133-dd07-4a1a-b282-f7770c372fb8')
    def test_update_access_control_list(self):
        """
        test method for update access control list
        """
        sec_group = self._create_security_groups()
        new_ctrl_list = self._create_access_control_lists(
            sec_group['name'])
        update_name = data_utils.rand_name('test')
        with self.rbac_utils.override_role(self):
            self.access_control_client.update_access_control_list(
                new_ctrl_list['uuid'],
                display_name=update_name)

    @decorators.idempotent_id('bb6a5a21-d8d1-489f-8002-e9eb07dfe873')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_access_control_list")
    @idempotent_id('36a8ace1-71ca-4c7c-8667-d8387d6f964a')
    def test_delete_access_control_list(self):
        """
        test method for delete access control list
        """
        # Create Security Group
        sec_group = self._create_security_groups()
        new_ctrl_list = self._create_access_control_lists(
            sec_group['name'])
        with self.rbac_utils.override_role(self):
            self.access_control_client.delete_access_control_list(
                new_ctrl_list['uuid'])
