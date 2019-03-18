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
Tempest test-case to test QoS Queue using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

LOG = logging.getLogger(__name__)
CONF = config.CONF


class QosQueueContrailTest(rbac_base.BaseContrailTest):
    """Test class to test QoS Queue using RBAC roles"""

    def _delete_qos_queue(self, qos_queue_id):
        self.qos_client.delete_qos_queue(qos_queue_id)

    def _create_qos_queues(self):
        name = data_utils.rand_name('test-rbac-qos-queue')
        if rbac_base.get_contail_version() < 5:
            fq_name = [name]
        else:
            fq_name = ['default-global-system-config',
                       "default-global-qos-config", name]
        qos_queue = self.qos_client.create_qos_queues(
            fq_name=fq_name)['qos-queue']
        self.addCleanup(self._try_delete_resource,
                        self._delete_qos_queue,
                        qos_queue['uuid'])
        return qos_queue

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_qos_queues"])
    @decorators.idempotent_id('3d3a4397-2afe-4bbd-be59-56a1bcc2e49d')
    def test_list_qos_queues(self):
        """test method for listing QoS queues"""
        self._create_qos_queues()
        with self.override_role():
            self.qos_client.list_qos_queues()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_qos_queues"])
    @decorators.idempotent_id('d89c45f4-c83c-47b3-8720-7feffab4519c')
    def test_create_qos_queues(self):
        """test method for creating QoS queues"""
        with self.override_role():
            self._create_qos_queues()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_qos_queue"])
    @decorators.idempotent_id('d2773d5c-9858-4938-8a77-62cafd5034da')
    def test_show_qos_queue(self):
        """test method for showing QoS queues"""
        qos_queue = self._create_qos_queues()
        with self.override_role():
            self.qos_client.show_qos_queue(qos_queue['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_qos_queue"])
    @decorators.idempotent_id('64c828d0-6594-472b-a504-40915067c7bd')
    def test_delete_qos_queue(self):
        """test method for deleting QoS queues"""
        qos_queue = self._create_qos_queues()
        with self.override_role():
            self.qos_client.delete_qos_queue(qos_queue['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_qos_queue"])
    @decorators.idempotent_id('0733ab1a-f5aa-4e70-a011-174aa203dc33')
    def test_update_qos_queue(self):
        """test method for deleting QoS queues"""
        qos_queue = self._create_qos_queues()
        display_name = data_utils.rand_name('qos_queue')
        with self.override_role():
            self.qos_client.update_qos_queue(
                qos_queue_id=qos_queue['uuid'],
                display_name=display_name)
