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
Tempest test-case to test QoS config objects using RBAC roles
"""

from oslo_log import log as logging

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

from patrole_tempest_plugin import rbac_rule_validation

from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib.decorators import idempotent_id

LOG = logging.getLogger(__name__)
CONF = config.CONF


class QosContrailTest(rbac_base.BaseContrailTest):

    """
    Test class to test QoS Config objects using RBAC roles
    """

    @classmethod
    def resource_setup(cls):
        super(QosContrailTest, cls).resource_setup()

    def _create_global_system_config(self):
        config_name = data_utils.rand_name('test-config')
        parent_type = 'config-root'
        config_fq_name = [config_name]
        new_config = \
            self.config_client.create_global_system_configs(
                parent_type=parent_type,
                display_name=config_name,
                fq_name=config_fq_name)['global-system-config']
        self.addCleanup(self._try_delete_resource,
                        (self.config_client.
                         delete_global_system_config),
                        new_config['uuid'])
        return new_config

    def _delete_qos_global_config(self, instance_id):
        return self.qos_client.delete_global_qos_config(instance_id)

    def _create_qos_global_configs(self, global_system_config):
        name = data_utils.rand_name('test-rbac-qos-global-config')
        parent_type = 'global-system-config'
        fq_name = [global_system_config, name]
        qos_global_config = self.qos_client.create_global_qos_configs(
            fq_name=fq_name,
            parent_type=parent_type)['global-qos-config']

        self.addCleanup(self._try_delete_resource,
                        self._delete_qos_global_config,
                        qos_global_config['uuid'])
        return qos_global_config

    @rbac_rule_validation.action(service="Contrail",
                                 rule="list_global_qos_configs")
    @idempotent_id('74e5a7b7-f538-4be3-90a5-6862b07fb118')
    def test_list_global_qos_configs(self):
        """
        test method for list global QoS objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        self._create_qos_global_configs(global_system_config)
        with self.rbac_utils.override_role(self):
            self.qos_client.list_global_qos_configs()

    @rbac_rule_validation.action(service="Contrail",
                                 rule="create_global_qos_configs")
    @idempotent_id('d7da1ca0-7bf7-4d1b-982c-820cd37fe9fa')
    def test_create_global_qos_configs(self):
        """
        test method for create global QoS objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        with self.rbac_utils.override_role(self):
            self._create_qos_global_configs(global_system_config)

    @rbac_rule_validation.action(service="Contrail",
                                 rule="show_global_qos_config")
    @idempotent_id('e3bd44e0-19a9-46e7-83d3-268dcc537ad9')
    def test_show_global_qos_config(self):
        """
        test method for show global QoS objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        test = self._create_qos_global_configs(global_system_config)
        with self.rbac_utils.override_role(self):
            self.qos_client.show_global_qos_config(instance_id=test['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rule="update_global_qos_config")
    @idempotent_id('f834c4d7-bc81-4c59-bada-c4d752219a6e')
    def test_update_global_qos_config(self):
        """
        test method for update global QoS objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        qos = self._create_qos_global_configs(global_system_config)
        display_name = data_utils.rand_name('qos_globale_config')
        with self.rbac_utils.override_role(self):
            self.qos_client.update_global_qos_config(
                instance_id=qos['uuid'],
                display_name=display_name)

    @rbac_rule_validation.action(service="Contrail",
                                 rule="delete_global_qos_config")
    @idempotent_id('78b9a3da-4eb1-4f4b-8a23-a8a2e733b515')
    def test_delete_global_qos_config(self):
        """
        test method for delete global QoS objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        qos_global_config = self._create_qos_global_configs(
            global_system_config)
        with self.rbac_utils.override_role(self):
            self.qos_client.delete_global_qos_config(qos_global_config['uuid'])
