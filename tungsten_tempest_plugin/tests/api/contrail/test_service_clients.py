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
Tempest test-case to test service clients objects using RBAC roles
"""

from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF


class ServiceClientsTest(rbac_base.BaseContrailTest):
    """Tempest test-case to test service clients objects using RBAC roles"""

    def _create_service_template(self):
        template_name = data_utils.rand_name('test-template')
        domain_name = 'default-domain'
        parent_type = 'domain'
        template_fq_name = ['default-domain', template_name]
        new_template = \
            self.service_client.create_service_templates(
                domain_name=domain_name,
                parent_type=parent_type,
                display_name=template_name,
                fq_name=template_fq_name)['service-template']
        self.addCleanup(self._try_delete_resource,
                        (self.service_client.
                         delete_service_template),
                        new_template['uuid'])
        return new_template

    def _create_service_health_check(self):
        health_check_name = data_utils.rand_name('test-health-check')
        domain_name = 'default-domain'
        parent_type = 'project'
        health_check_fq_name = ['default-domain', self.tenant_name,
                                health_check_name]
        new_health_check = \
            self.service_client.create_service_health_checks(
                domain_name=domain_name,
                parent_type=parent_type,
                display_name=health_check_name,
                fq_name=health_check_fq_name)['service-health-check']
        self.addCleanup(self._try_delete_resource,
                        (self.service_client.
                         delete_service_health_check),
                        new_health_check['uuid'])
        return new_health_check

    def _create_service_instance(self):
        instance_name = data_utils.rand_name('test-instance')
        domain_name = 'default-domain'
        parent_type = 'project'
        instance_fq_name = ['default-domain', self.tenant_name, instance_name]
        new_instance = \
            self.service_client.create_service_instances(
                domain_name=domain_name,
                fq_name=instance_fq_name,
                display_name=instance_name,
                parent_type=parent_type)['service-instance']
        self.addCleanup(self._try_delete_resource,
                        (self.service_client.
                         delete_service_instance),
                        new_instance['uuid'])
        return new_instance

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_service_templates"])
    @decorators.idempotent_id('841b1d32-4308-4fb6-852a-41bdd8c56c37')
    def test_list_service_templates(self):
        """test method for list service template objects"""
        with self.override_role():
            self.service_client.list_service_templates()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_service_templates"])
    @decorators.idempotent_id('3f02d14a-31e2-4476-821f-87d0cc42d9fb')
    def test_create_service_templates(self):
        """test method for create service template objects"""
        with self.override_role():
            self._create_service_template()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_service_template"])
    @decorators.idempotent_id('1f15d734-2cc6-4ded-916e-134286c6b87b')
    def test_show_service_template(self):
        """test method for show service template objects"""
        new_template = self._create_service_template()
        with self.override_role():
            self.service_client.show_service_template(
                new_template['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_service_template"])
    @decorators.idempotent_id('3549debd-4c7a-4574-8d11-4190c8530a23')
    def test_update_service_template(self):
        """test method for update service template objects"""
        new_template = self._create_service_template()
        update_name = data_utils.rand_name('test')
        with self.override_role():
            self.service_client.update_service_template(
                new_template['uuid'],
                display_name=update_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_service_template"])
    @decorators.idempotent_id('e86cabd2-5b7e-4ee8-86ec-db52619b852b')
    def test_delete_service_template(self):
        """test method for delete service template objects"""
        new_template = self._create_service_template()
        with self.override_role():
            self.service_client.delete_service_template(
                new_template['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_service_health_checks"])
    @decorators.idempotent_id('5210d6ca-9a38-4b6b-b5b7-f836c3846079')
    def test_list_service_health_checks(self):
        """test method for list service health check objects"""
        with self.override_role():
            self.service_client.list_service_health_checks()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_service_health_checks"])
    @decorators.idempotent_id('77716feb-0d05-4cfd-8a17-79cf0b19ed3c')
    def test_create_service_health(self):
        """test method for create service health check objects"""
        with self.override_role():
            self._create_service_health_check()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_service_health_check"])
    @decorators.idempotent_id('80db4445-8d6c-4c8f-aa25-d4ea53d32d2c')
    def test_show_service_health(self):
        """test method for show service health check objects"""
        new_health_check = self._create_service_health_check()
        with self.override_role():
            self.service_client.show_service_health_check(
                new_health_check['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_service_health_check"])
    @decorators.idempotent_id('68fb1510-4b76-40cc-8979-e56e537229d2')
    def test_update_service_health(self):
        """test method for update service health check objects"""
        new_health_check = self._create_service_health_check()
        update_name = data_utils.rand_name('test')
        with self.override_role():
            self.service_client.update_service_health_check(
                new_health_check['uuid'],
                display_name=update_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_service_health_check"])
    @decorators.idempotent_id('2dce3942-402a-48a4-b682-fdc425d3d935')
    def test_delete_service_health(self):
        """test method for delete service health check objects"""
        new_health_check = self._create_service_health_check()
        with self.override_role():
            self.service_client.delete_service_health_check(
                new_health_check['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_service_instances"])
    @decorators.idempotent_id('1469c71e-f6f5-419f-9672-c3c67f879704')
    def test_create_service_instances(self):
        """test method for create service client objects"""
        with self.override_role():
            self._create_service_instance()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_service_instance"])
    @decorators.idempotent_id('ea5b716d-5de8-4c71-becd-f1501c22f0df')
    def test_show_service_instance(self):
        """test method for show service client objects"""
        new_instance = self._create_service_instance()
        with self.override_role():
            self.service_client.show_service_instance(
                new_instance['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_service_instance"])
    @decorators.idempotent_id('74934833-29cd-416b-a5a6-273f733d058a')
    def test_delete_service_instance(self):
        """test method for delete service client objects"""
        new_instance = self._create_service_instance()
        with self.override_role():
            self.service_client.delete_service_instance(
                new_instance['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_service_instances"])
    @decorators.idempotent_id('da6016a3-a2a8-42a8-b064-c124c22fef6f')
    def test_list_service_instances(self):
        """test method for list service client objects"""
        with self.override_role():
            self.service_client.list_service_instances()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_service_instance"])
    @decorators.idempotent_id('a6237b99-336b-42db-a8eb-9604a1b08fc6')
    def test_update_service_instance(self):
        """test method for update service client objects"""
        new_instance = self._create_service_instance()
        update_name = data_utils.rand_name('test')
        with self.override_role():
            self.service_client.update_service_instance(
                new_instance['uuid'],
                display_name=update_name)
