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
Tempest test-case to test port tuple objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class ContrailPortTupleTest(rbac_base.BaseContrailTest):
    """Test class to test port tuple objects using RBAC roles"""

    @classmethod
    def resource_setup(cls):
        super(ContrailPortTupleTest, cls).resource_setup()
        instance_name = data_utils.rand_name('port-tuple-service-instance')
        domain_name = 'default-domain'
        parent_type = 'project'
        instance_fq_name = ['default-domain', cls.tenant_name, instance_name]
        cls.service_instance = \
            cls.service_client.create_service_instances(
                domain_name=domain_name,
                fq_name=instance_fq_name,
                display_name=instance_name,
                parent_type=parent_type)['service-instance']

    @classmethod
    def resource_cleanup(cls):
        cls._try_delete_resource(cls.service_client.delete_service_instance,
                                 cls.service_instance['uuid'])
        super(ContrailPortTupleTest, cls).resource_cleanup()

    def _create_port_tuple(self):
        tuple_name = data_utils.rand_name('port-tuple')
        fq_name = ['default-domain',
                   self.tenant_name,
                   self.service_instance['name'],
                   tuple_name]
        post_data = {
            'fq_name': fq_name,
            'parent_type': 'service-instance',
        }
        new_tuple = self.port_tuple_client.create_port_tuples(
            **post_data)['port-tuple']
        self.addCleanup(self._try_delete_resource,
                        self.port_tuple_client.delete_port_tuple,
                        new_tuple['uuid'])
        return new_tuple

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_port_tuples"])
    @decorators.idempotent_id('3789eef8-0e80-4057-b7b0-926655144beb')
    def test_list_port_tuples(self):
        """test method for list port tuple objects"""
        with self.override_role():
            self.port_tuple_client.list_port_tuples()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_port_tuple"])
    @decorators.idempotent_id('ae5a90ed-5771-4680-be6b-c7626caa3a52')
    def test_show_port_tuple(self):
        """test method for show port tuple objects"""
        new_tuple = self._create_port_tuple()
        with self.override_role():
            self.port_tuple_client.show_port_tuple(new_tuple['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_port_tuples"])
    @decorators.idempotent_id('0e2283da-fe25-4204-b5b3-fef3c200d0c8')
    def test_create_port_tuples(self):
        """test method for create port tuple objects"""
        with self.override_role():
            self._create_port_tuple()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_port_tuple"])
    @decorators.idempotent_id('b16f19e2-ec8e-4107-961d-561890183dd0')
    def test_update_port_tuple(self):
        """test method for update port tuple objects"""
        new_tuple = self._create_port_tuple()
        update_name = data_utils.rand_name('updated_tuple')
        with self.override_role():
            self.port_tuple_client.update_port_tuple(
                new_tuple['uuid'], display_name=update_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_port_tuple"])
    @decorators.idempotent_id('3f28e8b8-f9de-437f-a398-0a11c7fcd652')
    def test_delete_port_tuple(self):
        """test method for delete port tuple objects"""
        new_tuple = self._create_port_tuple()
        with self.override_role():
            self.port_tuple_client.delete_port_tuple(new_tuple['uuid'])
