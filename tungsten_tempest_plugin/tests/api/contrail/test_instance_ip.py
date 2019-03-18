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
Tempest test-case to test instance IP objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class InstanceIPTest(rbac_base.BaseContrailTest):
    """Test class to test instance IP objects using RBAC roles"""

    @classmethod
    def resource_setup(cls):
        super(InstanceIPTest, cls).resource_setup()
        # Create network ipam
        ipam_name = data_utils.rand_name('rbac-iip-ipam')
        fq_name_ipam = ['default-domain',
                        cls.tenant_name,
                        ipam_name]
        subnet_ip_prefix = {'ip_prefix': '1.2.3.0', 'ip_prefix_len': 24}
        ipam_post_body = {'display_name': ipam_name,
                          'fq_name': fq_name_ipam,
                          'parent_type': 'project'}
        body = cls.network_ipams_client.create_network_ipams(**ipam_post_body)
        cls.ipam = body['network-ipam']

        # Create network
        net_name = data_utils.rand_name('rbac-iip-network')
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
        super(InstanceIPTest, cls).resource_cleanup()

    def _create_instance_ip(self):
        iip_name = data_utils.rand_name('rbac-iip')
        virtual_network_refs = [
            {
                'to': self.network['fq_name'],
                'href': self.network['href'],
                'uuid': self.network['uuid']
            }
        ]
        post_body = {
            'display_name': iip_name,
            'fq_name': [iip_name],
            'virtual_network_refs': virtual_network_refs,
            'instance_ip_address': '1.2.3.50'
        }
        body = self.iip_client.create_instance_ips(**post_body)
        iip = body['instance-ip']
        self.addCleanup(self._try_delete_resource,
                        self.iip_client.delete_instance_ip,
                        iip['uuid'])
        return iip

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_instance_ips"])
    @decorators.idempotent_id('31db3b3f-c40b-4f7f-bb8b-0a110f099553')
    def test_list_instance_ips(self):
        """test method for list instance IP objects"""
        self._create_instance_ip()
        with self.override_role():
            self.iip_client.list_instance_ips()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_instance_ips"])
    @decorators.idempotent_id('78f5cd4d-345d-4d87-8b8b-4d5d3fec4a12')
    def test_create_instance_ips(self):
        """test method for create instance IP objects"""
        with self.override_role():
            self._create_instance_ip()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_instance_ip"])
    @decorators.idempotent_id('276f3838-d9cb-4432-bbb4-db31c4c1db5c')
    def test_show_instance_ip(self):
        """test method for update instance IP objects"""
        uuid = self._create_instance_ip()['uuid']
        with self.override_role():
            self.iip_client.show_instance_ip(uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_instance_ip"])
    @decorators.idempotent_id('b85975a5-176f-44b1-a615-b6f0a39a7708')
    def test_update_instance_ip(self):
        """test method for update instance IP objects"""
        uuid = self._create_instance_ip()['uuid']
        with self.override_role():
            self.iip_client.update_instance_ip(
                uuid,
                display_name='rbac-iip-new-name')

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_instance_ip"])
    @decorators.idempotent_id('d9c1d400-1dfb-4adb-8d97-0e8b498226b7')
    def test_delete_instance_ip(self):
        """test method for delete instance IP objects"""
        uuid = self._create_instance_ip()['uuid']
        with self.override_role():
            self.iip_client.delete_instance_ip(uuid)
