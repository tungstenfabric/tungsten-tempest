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
Tempest test-case to test virtual machines objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

LOG = logging.getLogger(__name__)
CONF = config.CONF


class VMContrailTest(rbac_base.BaseContrailTest):
    """Test class to test vm objects using RBAC roles"""

    @classmethod
    def resource_setup(cls):
        super(VMContrailTest, cls).resource_setup()
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
                     ]
                     }
        body = cls.vn_client.create_virtual_networks(**post_body)
        cls.network = body['virtual-network']

    def _delete_virtual_machine_interface(self, instance_id):
        return self.vm_client.delete_vm_interface(instance_id)

    def _create_virual_machine_interface(self):
        to_vm = ["default-domain", self.tenant_name, self.network['name']]
        net_id = self.network['uuid']
        virtual_network_refs = {"uuid": net_id,
                                "to": to_vm}
        name = data_utils.rand_name('vitual-machine-interface')
        domain_name = 'default-domain'
        fq_name = ['default-domain', self.tenant_name, name]
        parent_type = 'project'
        interface = self.vm_client.create_vm_interfaces(
            fq_name=fq_name,
            domain_name=domain_name,
            parent_type=parent_type,
            virtual_network_refs=[virtual_network_refs]
            )['virtual-machine-interface']
        self.addCleanup(self._try_delete_resource,
                        self._delete_virtual_machine_interface,
                        interface['uuid'])
        return interface

    @classmethod
    def resource_cleanup(cls):
        cls._try_delete_resource(cls.vn_client.delete_virtual_network,
                                 cls.network['uuid'])
        cls._try_delete_resource(cls.network_ipams_client.delete_network_ipam,
                                 cls.ipam['uuid'])
        super(VMContrailTest, cls).resource_cleanup()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_virtual_machine_interfaces"])
    @decorators.idempotent_id('e27d1fae-7324-4ef3-87b1-e7f519b1e2a7')
    def test_list_vm_interfaces(self):
        """test method for list vm interfaces objects"""
        self._create_virual_machine_interface()
        with self.override_role():
            self.vm_client.list_virtual_machine_interfaces()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_virtual_machine_interfaces"])
    @decorators.idempotent_id('d8a3a524-d61b-4bcb-8146-c5d4f308df8e')
    def test_add_vm_interfaces(self):
        """test method for add vm interfaces objects"""
        with self.override_role():
            self._create_virual_machine_interface()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_virtual_machine_interface"])
    @decorators.idempotent_id('3f17125a-9060-4c4a-a23f-0fe2aba2ccef')
    def test_show_vm_interface(self):
        """test method for show vm interfaces objects"""
        test = self._create_virual_machine_interface()
        with self.override_role():
            self.vm_client.show_virtual_machine_interface(test['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_virtual_machine_interface"])
    @decorators.idempotent_id('ce7f9471-ba1b-40d2-94f1-bdd0c610e22f')
    def test_delete_vm_interface(self):
        """test method for delete vm interfaces objects"""
        body = self._create_virual_machine_interface()
        with self.override_role():
            self.vm_client.delete_vm_interface(body['uuid'])

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_virtual_machine_interface"])
    @decorators.idempotent_id('7ca3046a-6245-4c15-914b-5a8ecdbeee11')
    def test_update_vm_interface(self):
        """test method for update vm interfaces objects"""
        virtual_machine = self._create_virual_machine_interface()
        display_name = data_utils.rand_name('new-vitual-machine-inf-name')
        with self.override_role():
            self.vm_client.update_vm_interface(
                instance_id=virtual_machine['uuid'],
                display_name=display_name)
