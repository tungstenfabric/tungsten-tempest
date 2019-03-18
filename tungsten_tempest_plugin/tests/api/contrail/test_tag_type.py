"""Tempest Suite for Tag Type of Contrail."""
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


class ContrailTagTypeTest(rbac_base.BaseContrailTest):
    """Test suite for validating RBAC functionality of 'tag-type' API."""

    @classmethod
    def skip_checks(cls):
        """Skip the checks if contrail Version is less than 4.1."""
        super(ContrailTagTypeTest, cls).skip_checks()
        if float(CONF.sdn.contrail_version) < 4.1:
            msg = "tag-type requires Contrail >= 4.1"
            raise cls.skipException(msg)

    @classmethod
    def resource_setup(cls):
        """Create Tag type to use it across the Suite."""
        super(ContrailTagTypeTest, cls).resource_setup()
        cls.tag_type_uuid = cls._create_tag_type()

    @classmethod
    def _create_tag_type(cls):
        """Create Tag type."""
        tag_type_name = data_utils.rand_name('tag-type')
        fq_name = [tag_type_name]
        post_data = {'fq_name': fq_name}
        new_tag_type = cls.contrail_client.create_tag_type(
            **post_data)['tag-type']
        tag_type_uuid = new_tag_type['uuid']
        cls.addClassResourceCleanup(
            cls._try_delete_resource,
            cls.contrail_client.delete_tag_type,
            tag_type_uuid)
        return tag_type_uuid

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_tag_types"])
    @decorators.idempotent_id('53c34f3a-f426-11e8-8eb2-f2801f1b9fd1')
    def test_list_tag_types(self):
        """List tag-type.

        RBAC test for contrail list tag_type policy
        """
        with self.override_role():
            self.contrail_client.list_tag_types()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_tag_type"])
    @decorators.idempotent_id('64cf8892-f427-11e8-8eb2-f2801f1b9fd1')
    def test_show_tag_type(self):
        """Show tag-type.

        RBAC test for contrail show tag_type policy
        """
        with self.override_role():
            self.contrail_client.show_tag_type(self.tag_type_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_tag_types"])
    @decorators.idempotent_id('7e602032-f427-11e8-8eb2-f2801f1b9fd1')
    def test_create_tag_types(self):
        """Create tag-type.

        RBAC test for contrail create tag_type policy
        """
        with self.override_role():
            self._create_tag_type()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_tag_type"])
    @decorators.idempotent_id('98f6beba-f427-11e8-8eb2-f2801f1b9fd1')
    def test_update_tag_type(self):
        """Update tag-type.

        RBAC test for contrail update tag_type policy
        """
        update_name = data_utils.rand_name('new_name')
        with self.override_role():
            self.contrail_client.update_tag_type(
                self.tag_type_uuid, name=update_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_tag_type"])
    @decorators.idempotent_id('b0f81fae-f427-11e8-8eb2-f2801f1b9fd1')
    def test_delete_tag_type(self):
        """Delete tag-type.

        RBAC test for contrail delete tag_type policy
        """
        new_tag_type_uuid = self._create_tag_type()
        with self.override_role():
            self.contrail_client.delete_tag_type(new_tag_type_uuid)
