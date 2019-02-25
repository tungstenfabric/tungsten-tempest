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
Tempest test-case to test load balancer objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators
from tempest import test

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class BaseLoadBalancerTest(rbac_base.BaseContrailTest):
    """Base class to test load balancer objects using RBAC roles"""

    @classmethod
    def skip_checks(cls):
        super(BaseLoadBalancerTest, cls).skip_checks()
        if not test.is_extension_enabled('lbaas', 'network'):
            raise cls.skipException(
                '%s skipped - lbaas extension not enabled' % cls.__name__)

    def _create_load_balancer(self):
        fq_name = data_utils.rand_name('load-balancer')
        post_body = {
            'parent_type': 'project',
            'fq_name': ['default-domain', self.tenant_name, fq_name]
        }
        resp_body = self.load_balancer_client.create_load_balancers(
            **post_body)
        lb_uuid = resp_body['loadbalancer']['uuid']
        self.addCleanup(self._try_delete_resource,
                        self.load_balancer_client.delete_load_balancer,
                        lb_uuid)
        return lb_uuid

    def _update_load_balancer(self, lb_uuid):
        put_body = {
            'display_name': data_utils.rand_name('load-balancer')
        }
        self.load_balancer_client.update_load_balancer(lb_uuid, **put_body)

    def _create_load_balancer_health_monitor(self):
        fq_name = data_utils.rand_name('load_balancer-health-monitor')
        post_body = {
            'parent_type': 'project',
            'fq_name': ['default-domain', self.tenant_name, fq_name],
            'loadbalancer_healthmonitor_properties': {
                'monitor_type': 'PING',
                'delay': 10,
                'timeout': 60,
                'max_retries': 3
            }
        }
        resp_body = self.load_balancer_client \
            .create_lb_healthmonitors(**post_body)
        lb_hm_uuid = resp_body['loadbalancer-healthmonitor']['uuid']
        self.addCleanup(self._try_delete_resource,
                        self.load_balancer_client
                        .delete_lb_healthmonitor,
                        lb_hm_uuid)
        return lb_hm_uuid

    def _update_load_balancer_health_monitor(self, lb_hm_uuid):
        display_name = data_utils.rand_name('load_balancer-health-monitor')
        put_body = {
            'display_name': display_name
        }

        self.load_balancer_client.update_lb_healthmonitor(
            lb_hm_uuid,
            **put_body)

    def _create_load_balancer_listener(self):
        fq_name = data_utils.rand_name('load_balancer-listener')
        post_body = {
            'parent_type': 'project',
            'fq_name': ['default-domain', self.tenant_name, fq_name]
        }
        resp_body = self.load_balancer_client.create_load_balancer_listeners(
            **post_body)
        lb_listener_uuid = resp_body['loadbalancer-listener']['uuid']
        self.addCleanup(self._try_delete_resource,
                        self.load_balancer_client
                        .delete_load_balancer_listener,
                        lb_listener_uuid)
        return lb_listener_uuid

    def _update_load_balancer_listener(self, lb_listener_uuid):
        put_body = {
            'display_name': data_utils.rand_name('load_balancer-listener')
        }
        self.load_balancer_client.update_load_balancer_listener(
            lb_listener_uuid,
            **put_body)

    def _create_load_balancer_pool(self, return_object=False):
        fq_name = data_utils.rand_name('load_balancer-pool')
        post_body = {
            'parent_type': 'project',
            'fq_name': ['default-domain', self.tenant_name, fq_name]
        }
        resp_body = self.load_balancer_client.create_load_balancer_pools(
            **post_body)
        lb_pool_uuid = resp_body['loadbalancer-pool']['uuid']
        self.addCleanup(self._try_delete_resource,
                        self.load_balancer_client.delete_load_balancer_pool,
                        lb_pool_uuid)
        if return_object:
            return resp_body['loadbalancer-pool']
        return lb_pool_uuid

    def _update_load_balancer_pool(self, lb_pool_uuid):
        put_body = {
            'display_name': data_utils.rand_name('load_balancer-pool')
        }
        self.load_balancer_client.update_load_balancer_pool(lb_pool_uuid,
                                                            **put_body)

    def _create_load_balancer_member(self):
        lb_pool = self._create_load_balancer_pool(return_object=True)
        fq_name = data_utils.rand_name('load_balancer-member')
        post_body = {
            'parent_type': 'loadbalancer-pool',
            'fq_name': ['default-domain', self.tenant_name, lb_pool['name'],
                        fq_name]
        }
        resp_body = self.load_balancer_client.create_load_balancer_members(
            **post_body)
        lb_member_uuid = resp_body['loadbalancer-member']['uuid']
        self.addCleanup(self._try_delete_resource,
                        self._delete_pool_and_member,
                        lb_pool['uuid'],
                        lb_member_uuid)
        return lb_member_uuid

    def _update_load_balancer_member(self, lb_member_uuid):
        put_body = {
            'display_name': data_utils.rand_name('load_balancer-member')
        }
        self.load_balancer_client.update_load_balancer_member(lb_member_uuid,
                                                              **put_body)

    def _delete_pool_and_member(self, lb_pool_uuid, lb_member_uuid):
        # Used by _try_delete_resource in _create_load_balancer_member.
        # Guarantees that child (lb member) is deleted before parent
        # dependency (lb pool).
        self.load_balancer_client.delete_load_balancer_member(lb_member_uuid)
        self.load_balancer_client.delete_load_balancer_pool(lb_pool_uuid)


class LoadBalancerContrailTest(BaseLoadBalancerTest):
    """Test class to test load balancer objects using RBAC roles"""

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_load_balancers"])
    @decorators.idempotent_id('5d840b6b-3974-4945-916f-dd53ba27e42f')
    def test_list_load_balancers(self):
        """test method for list load balancer objects"""
        with self.override_role():
            self.load_balancer_client.list_load_balancers()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_load_balancers"])
    @decorators.idempotent_id('6a18d506-0794-4eb9-a945-165bf146005d')
    def test_create_load_balancers(self):
        """test method for create load balancer objects"""
        with self.override_role():
            self._create_load_balancer()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_load_balancer"])
    @decorators.idempotent_id('428012aa-cd0e-4702-89d2-459046d4bd5f')
    def test_show_load_balancer(self):
        """test method for show load balancer objects"""
        lb_uuid = self._create_load_balancer()
        with self.override_role():
            self.load_balancer_client.show_load_balancer(lb_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_load_balancer"])
    @decorators.idempotent_id('7cd3d7b2-b149-40c1-a801-a6a8a660bd24')
    def test_update_load_balancer(self):
        """test method for update load balancer objects"""
        lb_uuid = self._create_load_balancer()
        with self.override_role():
            self._update_load_balancer(lb_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_load_balancer"])
    @decorators.idempotent_id('b28c6b11-d1b0-45d0-8942-638b6b590702')
    def test_delete_load_balancer(self):
        """test method for delete load balancer objects"""
        lb_uuid = self._create_load_balancer()
        with self.override_role():
            self.load_balancer_client.delete_load_balancer(lb_uuid)


class LoadBalancerHealthMonitorContrailTest(BaseLoadBalancerTest):
    """Test class to test load balancer Health Monitor objects using RBAC roles

    """

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_load_balancer_health_monitors"])
    @decorators.idempotent_id('3e3d8bdc-3621-4c5e-8130-1187f445a4e6')
    def test_list_lb_health_monitors(self):
        """test method for list load balancer health monitor objects"""
        with self.override_role():
            self.load_balancer_client.list_lb_healthmonitors()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_load_balancer_health_monitors"]
                                 )
    @decorators.idempotent_id('bddb93ad-d331-4bbc-bac6-2763cae4eb2c')
    def test_create_lb_health_monitors(self):
        """test method for create load balancer health monitor objects"""
        with self.override_role():
            self._create_load_balancer_health_monitor()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_load_balancer_health_monitor"])
    @decorators.idempotent_id('30d23994-1e3a-4a76-8f18-e00d0854412a')
    def test_show_lb_health_monitor(self):
        """test method for show load balancer health monitor objects"""
        lb_hm_uuid = self._create_load_balancer_health_monitor()
        with self.override_role():
            self.load_balancer_client.show_lb_healthmonitor(
                lb_hm_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_load_balancer_health_monitor"])
    @decorators.idempotent_id('c32ba92c-3a69-4255-867a-1423c93faa6f')
    def test_update_lb_health_monitor(self):
        """test method for update load balancer health monitor objects"""
        lb_hm_uuid = self._create_load_balancer_health_monitor()
        with self.override_role():
            self._update_load_balancer_health_monitor(lb_hm_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_load_balancer_health_monitor"])
    @decorators.idempotent_id('b4d7ea9d-fd8c-433b-96fc-c24866b3f6a7')
    def test_delete_lb_health_monitor(self):
        """test method for delete load balancer health monitor objects"""
        lb_hm_uuid = self._create_load_balancer_health_monitor()
        with self.override_role():
            self.load_balancer_client.delete_lb_healthmonitor(
                lb_hm_uuid)


class LoadBalancerListenerContrailTest(BaseLoadBalancerTest):
    """Base class to test load balancer Listener objects using RBAC roles"""

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_load_balancer_listeners"])
    @decorators.idempotent_id('7e02882f-0eab-41c2-b48a-bf71e083b912')
    def test_list_lb_listeners(self):
        """test method for list load balancer listener objects"""
        with self.override_role():
            self.load_balancer_client.list_load_balancer_listeners()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_load_balancer_listeners"])
    @decorators.idempotent_id('0551de87-fa4c-463f-8968-ec6f2a6098d0')
    def test_create_lb_listeners(self):
        """test method for create load balancer listener objects"""
        with self.override_role():
            self._create_load_balancer_listener()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_load_balancer_listener"])
    @decorators.idempotent_id('ade38959-9506-4262-8d3c-5ba5eb63d85f')
    def test_show_lb_listener(self):
        """test method for show load balancer listener objects"""
        lb_listener_uuid = self._create_load_balancer_listener()
        with self.override_role():
            self.load_balancer_client.show_load_balancer_listener(
                lb_listener_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_load_balancer_listener"])
    @decorators.idempotent_id('e529e538-da31-4159-91c2-6c0a828282a4')
    def test_update_lb_listener(self):
        """test method for update load balancer listener objects"""
        lb_listener_uuid = self._create_load_balancer_listener()
        with self.override_role():
            self._update_load_balancer_listener(lb_listener_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_load_balancer_listener"])
    @decorators.idempotent_id('feaf3e9a-ffd1-4327-ad7a-35f9e9e4989b')
    def test_delete_lb_listener(self):
        """test method for delete load balancer listener objects"""
        lb_listener_uuid = self._create_load_balancer_listener()
        with self.override_role():
            self.load_balancer_client.delete_load_balancer_listener(
                lb_listener_uuid)


class LoadBalancerPoolContrailTest(BaseLoadBalancerTest):
    """Base class to test load balancer Pool objects using RBAC roles"""

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_load_balancer_pools"])
    @decorators.idempotent_id('3d177a9e-7067-4e9e-b4e8-0acc5887dff0')
    def test_list_load_balancer_pools(self):
        """test method for list load balancer pool objects"""
        with self.override_role():
            self.load_balancer_client.list_load_balancer_pools()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_load_balancer_pools"])
    @decorators.idempotent_id('a52c6ec7-a996-4191-9a70-7879a211a711')
    def test_create_load_balancer_pools(self):
        """test method for create load balancer pool objects"""
        with self.override_role():
            self._create_load_balancer_pool()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_load_balancer_pool"])
    @decorators.idempotent_id('7923da4e-53b1-4024-9a40-5bc91cee8e2d')
    def test_show_load_balancer_pool(self):
        """test method for show load balancer pool objects"""
        lb_pool_uuid = self._create_load_balancer_pool()
        with self.override_role():
            self.load_balancer_client.show_load_balancer_pool(lb_pool_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_load_balancer_pool"])
    @decorators.idempotent_id('391c0c5e-c218-4c98-9b58-6d2724ec4c20')
    def test_update_load_balancer_pool(self):
        """test method for update load balancer pool objects"""
        lb_pool_uuid = self._create_load_balancer_pool()
        with self.override_role():
            self._update_load_balancer_pool(lb_pool_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_load_balancer_pool"])
    @decorators.idempotent_id('8b3617c0-4064-48f8-96b8-e2f996fce5c3')
    def test_delete_load_balancer_pool(self):
        """test method for delete load balancer pool objects"""
        lb_pool_uuid = self._create_load_balancer_pool()
        with self.override_role():
            self.load_balancer_client.delete_load_balancer_pool(lb_pool_uuid)


class LoadBalancerMemberContrailTest(BaseLoadBalancerTest):
    """Base class to test load balancer Member using RBAC roles"""

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_load_balancer_members"])
    @decorators.idempotent_id('b3c51463-8166-486a-a26e-0f7aeaa41e0f')
    def test_list_load_balancer_members(self):
        """test method for list load balancer member objects"""
        with self.override_role():
            self.load_balancer_client.list_load_balancer_members()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_load_balancer_members"])
    @decorators.idempotent_id('ad60688f-7a20-4dd5-8229-4076d85b9d55')
    def test_create_lb_members(self):
        """test method for create load balancer member objects"""
        with self.override_role():
            self._create_load_balancer_member()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_load_balancer_member"])
    @decorators.idempotent_id('917602ff-24d5-4a07-a6a6-5e5b9539bbf1')
    def test_show_load_balancer_member(self):
        """test method for show load balancer member objects"""
        lb_member_uuid = self._create_load_balancer_member()
        with self.override_role():
            self.load_balancer_client.show_load_balancer_member(lb_member_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_load_balancer_member"])
    @decorators.idempotent_id('b1611005-5c77-4ac0-8fcc-4a035dfbaa84')
    def test_update_lb_member(self):
        """test method for update load balancer member objects"""
        lb_member_uuid = self._create_load_balancer_member()
        with self.override_role():
            self._update_load_balancer_member(lb_member_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_load_balancer_member"])
    @decorators.idempotent_id('dc21883a-a822-4d39-b815-4dfd6b505b0b')
    def test_delete_lb_member(self):
        """test method for delete load balancer member objects"""
        lb_member_uuid = self._create_load_balancer_member()
        with self.override_role():
            self.load_balancer_client.delete_load_balancer_member(
                lb_member_uuid)
