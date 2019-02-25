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
Tempest test-case to test floating IP objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class BaseFloatingIpTest(rbac_base.BaseContrailTest):
    """Base class to test floating IP objects using RBAC roles"""

    @classmethod
    def resource_setup(cls):
        super(BaseFloatingIpTest, cls).resource_setup()

        # Create subnet using ipam
        ipam_name = data_utils.rand_name('rbac-fip-ipam')
        fq_name_ipam = ['default-domain',
                        cls.tenant_name,
                        ipam_name]

        ip_cidr = CONF.network.project_network_cidr
        ip_prefix, ip_prefix_len = ip_cidr.split('/')
        subnet_ip_prefix = {'ip_prefix': ip_prefix,
                            'ip_prefix_len': int(ip_prefix_len)}
        ipam_post_body = {'parent_type': 'project', 'fq_name': fq_name_ipam}

        body = cls.network_ipams_client.create_network_ipams(**ipam_post_body)
        cls.ipam = body['network-ipam']

        # Create network
        net_name = data_utils.rand_name('rbac-pool-network')
        fq_name = ['default-domain', cls.tenant_name, net_name]

        post_body = {'parent_type': 'project',
                     'router_external': True,
                     'fq_name': fq_name,
                     'network_ipam_refs': [
                         {
                             'to': cls.ipam['fq_name'],
                             'href': cls.ipam['href'],
                             'uuid': cls.ipam['uuid'],
                             'attr': {
                                 'ipam_subnets': [{'subnet': subnet_ip_prefix}]
                             }
                         }
                     ],
                     'virtual_network_properties': {
                         'forwarding_mode': 'l3'
                     }
                     }
        body = cls.vn_client.create_virtual_networks(**post_body)
        cls.network = body['virtual-network']

    @classmethod
    def resource_cleanup(cls):
        cls._try_delete_resource(cls.vn_client.delete_virtual_network,
                                 cls.network['uuid'])
        cls._try_delete_resource(cls.network_ipams_client.delete_network_ipam,
                                 cls.ipam['uuid'])
        super(BaseFloatingIpTest, cls).resource_cleanup()


class FloatingIpPoolTest(BaseFloatingIpTest):
    """Test class to test Floating IP pool objects using RBAC roles"""

    def _create_floating_ip_pool(self):
        pool_name = data_utils.rand_name('rbac-fip-pool')
        fq_name = ['default-domain', self.tenant_name,
                   self.network['name'], pool_name]

        post_body = {'display_name': pool_name,
                     'parent_type': 'virtual-network',
                     'fq_name': fq_name}

        body = self.fip_client.create_floating_ip_pools(**post_body)
        fip_pool = body['floating-ip-pool']

        self.addCleanup(self._try_delete_resource,
                        self.fip_client.delete_floating_ip_pool,
                        fip_pool['uuid'])

        return fip_pool

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_floating_ip_pools"])
    @decorators.idempotent_id('a83ca5e8-be4b-4161-869c-f981a724cf82')
    def test_create_floating_ip_pools(self):
        """test method for create floating IP pool objects"""
        with self.override_role():
            self._create_floating_ip_pool()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_floating_ip_pools"])
    @decorators.idempotent_id('9d20e78d-0463-4a0e-b30c-40770bee35bc')
    def test_list_floating_ip_pools(self):
        """test method for list floating IP pool objects"""
        self._create_floating_ip_pool()
        with self.override_role():
            self.fip_client.list_floating_ip_pools()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_floating_ip_pool"])
    @decorators.idempotent_id('1ec3124c-c15c-4ee6-b2de-2feed9599e38')
    def test_show_floating_ip_pool(self):
        """test method for show floating IP pool objects"""
        uuid = self._create_floating_ip_pool()['uuid']
        with self.override_role():
            self.fip_client.show_floating_ip_pool(uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_floating_ip_pool"])
    @decorators.idempotent_id('6563f2e7-ae6b-483b-8c07-0111efc86817')
    def test_update_floating_ip_pool(self):
        """test method for update floating IP pool objects"""
        uuid = self._create_floating_ip_pool()['uuid']
        with self.override_role():
            self.fip_client.update_floating_ip_pool(
                uuid,
                display_name='rbac-fip-pool-new-name')

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_floating_ip_pool"])
    @decorators.idempotent_id('c4b449ae-2f12-49cf-9dec-2b21c143aff6')
    def test_delete_floating_ip_pool(self):
        """test method for delete floating IP pool objects"""
        uuid = self._create_floating_ip_pool()['uuid']
        with self.override_role():
            self.fip_client.delete_floating_ip_pool(uuid)


class FloatingIpTest(BaseFloatingIpTest):
    """Test class to test floating IP objects using RBAC roles"""

    @classmethod
    def resource_setup(cls):
        super(FloatingIpTest, cls).resource_setup()
        # Create Floating IP pool for the network
        pool_name = data_utils.rand_name('rbac-fip-pool')
        fq_name = ['default-domain', cls.tenant_name,
                   cls.network['name'], pool_name]
        post_body = {'parent_type': 'virtual-network', 'fq_name': fq_name}
        body = cls.fip_client.create_floating_ip_pools(**post_body)
        cls.fip_pool = body['floating-ip-pool']

    @classmethod
    def resource_cleanup(cls):
        cls._try_delete_resource(cls.fip_client.delete_floating_ip_pool,
                                 cls.fip_pool['uuid'])
        super(FloatingIpTest, cls).resource_cleanup()

    def _create_floating_ip(self):
        fip_name = data_utils.rand_name('rbac-fip')
        fq_name = ['default-domain', self.tenant_name, self.network['name'],
                   self.fip_pool['name'], fip_name]
        project_refs = {'to': ['default-domain', self.tenant_name]}
        post_body = {'display_name': fip_name,
                     'parent_type': 'floating-ip-pool',
                     'fq_name': fq_name,
                     'project_refs': [project_refs]}
        body = self.fip_client.create_floating_ips(**post_body)
        fip = body['floating-ip']
        self.addCleanup(self._try_delete_resource,
                        self.fip_client.delete_floating_ip,
                        fip['uuid'])
        return fip

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_floating_ips"])
    @decorators.idempotent_id('ff05f70f-9db9-43cb-a5ce-38cbbef2c430')
    def test_create_floating_ips(self):
        """test method for create floating IP objects"""
        with self.override_role():
            self._create_floating_ip()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_floating_ips"])
    @decorators.idempotent_id('e56046f9-32f9-41ce-9c1b-b982997ac347')
    def test_list_floating_ips(self):
        """test method for list floating IP objects"""
        self._create_floating_ip()
        with self.override_role():
            self.fip_client.list_floating_ips()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_floating_ip"])
    @decorators.idempotent_id('293f2c26-4101-4a2f-86d4-feb2878bd511')
    def test_show_floating_ip(self):
        """test method for show floating IP objects"""
        uuid = self._create_floating_ip()['uuid']
        with self.override_role():
            self.fip_client.show_floating_ip(uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_floating_ip"])
    @decorators.idempotent_id('a09283c9-73d3-42f7-876d-f33040686d6d')
    def test_update_floating_ip(self):
        """test method for update floating IP objects"""
        uuid = self._create_floating_ip()['uuid']
        with self.override_role():
            self.fip_client.update_floating_ip(
                uuid,
                display_name='rbac-fip-new-name')

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_floating_ip"])
    @decorators.idempotent_id('a26f162f-da56-4153-aed6-bffccba92bc7')
    def test_delete_floating_ip(self):
        """test method for delete floating IP objects"""
        uuid = self._create_floating_ip()['uuid']
        with self.override_role():
            self.fip_client.delete_floating_ip(uuid)
