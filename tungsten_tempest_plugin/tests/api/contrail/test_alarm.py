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
Tempest test-case to test Alarms object using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class AlarmContrailTest(rbac_base.BaseContrailTest):
    """Test class to test Alarm objects using RBAC roles"""

    def _create_alarm(self):
        post_body = {
            'fq_name': ['default-domain',
                        self.tenant_name,
                        data_utils.rand_name('alarm')],
            'alarm_severity': 1,
            'parent_type': 'project',
            'uve_keys': {
                'uve_key': ['virtual-network']
            },
            'alarm_rules': {
                'or_list': [{
                    'and_list': [{
                        'operation': '!=',
                        'operand1': data_utils.rand_name('tempest-alarm'),
                        'operand2': {
                            'uve_attribute': 'name'
                        }
                    }]
                }]
            }
        }

        resp_body = self.alarm_client.create_alarms(
            **post_body)
        alarm_uuid = resp_body['alarm']['uuid']
        self.addCleanup(self._try_delete_resource,
                        self.alarm_client.delete_alarm,
                        alarm_uuid)
        return alarm_uuid

    def _update_alarm(self, alarm_uuid):
        put_body = {
            'alarm_severity': 2
        }
        self.alarm_client.update_alarm(alarm_uuid, **put_body)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_alarms"])
    @decorators.idempotent_id('dc7d19dd-dd5e-4ec8-bf0c-c6d9d83a60a8')
    def test_list_alarms(self):
        """test method for list alarms"""
        with self.override_role():
            self.alarm_client.list_alarms()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_alarms"])
    @decorators.idempotent_id('7fe55d0c-e54a-4bb7-95a6-9c53f9e9c4bf')
    def test_create_alarms(self):
        """test method for create alarms"""
        with self.override_role():
            self._create_alarm()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_alarm"])
    @decorators.idempotent_id('ab0ccbe4-7bfe-4176-890a-d438ee04290d')
    def test_show_alarm(self):
        """test method for show alarms"""
        alarm_uuid = self._create_alarm()
        with self.override_role():
            self.alarm_client.show_alarm(alarm_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_alarm"])
    @decorators.idempotent_id('ab331cca-ee53-4106-9b30-7319bfb1bea7')
    def test_update_alarm(self):
        """test method for update alarms"""
        alarm_uuid = self._create_alarm()
        with self.override_role():
            self._update_alarm(alarm_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_alarm"])
    @decorators.idempotent_id('84fadb14-77c0-4f21-b5b2-1da7a2fd27e6')
    def test_delete_alarm(self):
        """test method for delete alarms"""
        # Create global system config
        alarm_uuid = self._create_alarm()
        with self.override_role():
            self.alarm_client.delete_alarm(alarm_uuid)
