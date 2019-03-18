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
Tempest test-case to test forwarding class objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class ContrailForwardingClassTest(rbac_base.BaseContrailTest):
    """Test class to test Forwarding class objects using RBAC roles"""

    def _create_qos_global_configs(self):
        name = data_utils.rand_name('test-rbac-qos-global-config')
        parent_type = 'global-system-config'
        fq_name = ['default-global-system-config', name]
        qos_global_config = self.qos_client.create_global_qos_configs(
            fq_name=fq_name,
            parent_type=parent_type)['global-qos-config']

        self.addCleanup(self._try_delete_resource,
                        self.qos_client.delete_global_qos_config,
                        qos_global_config['uuid'])
        return qos_global_config

    def _create_forwarding_class(self,
                                 global_qos_config):
        display_name = data_utils.rand_name('forwarding-class')
        parent_type = 'global-qos-config'
        fq_name = ['default-global-system-config', global_qos_config, "1"]
        forwarding_class_id = data_utils.rand_int_id(1, 200)
        post_data = {
            'fq_name': fq_name,
            'parent_type': parent_type,
            'display_name': display_name,
            'forwarding_class_id': forwarding_class_id
        }
        new_fclass = self.forwarding_class_client.create_forwarding_classs(
            **post_data)['forwarding-class']
        self.addCleanup(self._try_delete_resource,
                        self.forwarding_class_client.delete_forwarding_class,
                        new_fclass['uuid'])
        return new_fclass

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_forwarding_classs"])
    @decorators.idempotent_id('807a66fd-d4a4-472c-a13d-7ba590509e6e')
    def test_list_forwarding_classs(self):
        """test method for list forwarding classes objects"""
        with self.override_role():
            self.forwarding_class_client.list_forwarding_classs()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_forwarding_class"])
    @decorators.idempotent_id('8ef21f71-72a4-4de9-af93-6e759aa463c0')
    def test_show_forwarding_class(self):
        """test method for show forwarding classes objects"""
        # Create a global qos config
        self.global_qos_config = \
            self._create_qos_global_configs()['name']
        new_fclass = self._create_forwarding_class(self.global_qos_config)
        with self.override_role():
            self.forwarding_class_client.show_forwarding_class(
                new_fclass['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_forwarding_classs"])
    @decorators.idempotent_id('d098859c-ad36-4385-8fb0-c00934a99b6f')
    def test_create_forwarding_class(self):
        """test method for create forwarding classes objects"""
        # Create a global qos config
        self.global_qos_config = \
            self._create_qos_global_configs()['name']
        with self.override_role():
            self._create_forwarding_class(self.global_qos_config)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_forwarding_class"])
    @decorators.idempotent_id('589dc03d-a25d-48be-9d9c-d3f92ff2cfc6')
    def test_update_forwarding_class(self):
        """test method for update forwarding classes objects"""
        # Create a global qos config
        self.global_qos_config = \
            self._create_qos_global_configs()['name']
        new_fclass = self._create_forwarding_class(self.global_qos_config)
        update_name = data_utils.rand_name('updated_fclass')
        with self.override_role():
            self.forwarding_class_client.update_forwarding_class(
                new_fclass['uuid'], display_name=update_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_forwarding_class"])
    @decorators.idempotent_id('a0348ffc-68c5-4d94-ba03-d08483503ced')
    def test_delete_forwarding_class(self):
        """test method for delete forwarding classes objects"""
        # Create a global qos config
        self.global_qos_config = \
            self._create_qos_global_configs()['name']
        new_fclass = self._create_forwarding_class(self.global_qos_config)
        with self.override_role():
            self.forwarding_class_client.delete_forwarding_class(
                new_fclass['uuid'])
