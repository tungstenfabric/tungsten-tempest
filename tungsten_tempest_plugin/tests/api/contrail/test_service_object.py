"""Tempest Suite for Contrail Service Objects."""
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
from tempest.lib.decorators import idempotent_id

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF


class ServiceObjectContrailTest(rbac_base.BaseContrailTest):
    """Class to test the Service objects of Contrail."""

    @classmethod
    def skip_checks(cls):
        """Skip the suite if the Contrail version is less than 4.1."""
        super(ServiceObjectContrailTest, cls).skip_checks()
        if float(CONF.sdn.contrail_version) < 4.1:
            msg = "service_object requires Contrail >= 4.1"
            raise cls.skipException(msg)

    @classmethod
    def resource_setup(cls):
        """Create Service object to use it across the suite."""
        super(ServiceObjectContrailTest, cls).resource_setup()
        cls.service_object_uuid = cls._create_service_object()

    @classmethod
    def _create_service_object(cls):
        """Create service object."""
        display_name = data_utils.rand_name('service_object')
        post_body = {'display_name': display_name}
        post_body['fq_name'] = [display_name]
        resp_body = cls.contrail_client.create_service_object(**post_body)
        service_object_uuid = resp_body['service-object']['uuid']
        cls.addClassResourceCleanup(
            cls._try_delete_resource,
            cls.contrail_client.delete_service_object,
            service_object_uuid)
        return service_object_uuid

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_service_objects"])
    @decorators.idempotent_id('05458fa1-ba09-4772-91aa-ca06243b5f5e')
    def test_list_service_objects(self):
        """List service_objects.

        RBAC test for the Contrail list_service_objects policy
        """
        with self.rbac_utils.override_role(self):
            self.contrail_client.list_service_objects()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_service_object"])
    @decorators.idempotent_id('8be0e381-3abb-4256-858d-5930db4ceafb')
    def test_create_service_object(self):
        """Create service_object.

        RBAC test for the Contrail create_service_object policy
        """
        with self.rbac_utils.override_role(self):
            self._create_service_object()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_service_object"])
    @decorators.idempotent_id('bb570ddd-c5fa-4691-899e-00a64568f736')
    def test_show_service_object(self):
        """Show service_object.

        RBAC test for the Contrail show_service_object policy
        """
        with self.rbac_utils.override_role(self):
            self.contrail_client.show_service_object(self.service_object_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_service_object"])
    @decorators.idempotent_id('15a4d6dc-f16b-11e8-8e54-080027758b73')
    def test_delete_service_object(self):
        """Delete service_object.

        RBAC test for the Contrail delete_service_object policy
        """
        obj_uuid = self._create_service_object()
        with self.rbac_utils.override_role(self):
            self.contrail_client.delete_service_object(obj_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_service_object"])
    @decorators.idempotent_id('a6eaee65-9ead-4df5-9aa0-5329ee9a26f2')
    def test_update_service_object(self):
        """Update service_object.

        RBAC test for the Contrail update_service_object policy
        """
        put_body = {
            'display_name': data_utils.rand_name(
                'update_service_object')}
        with self.rbac_utils.override_role(self):
            self.contrail_client.update_service_object(
                self.service_object_uuid, **put_body)
