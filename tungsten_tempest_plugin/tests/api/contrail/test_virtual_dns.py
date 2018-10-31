# Copyright 2016 AT&T Corp
# All Rignhts Reserved.
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
Tempest test-case to test virtual dns objects using RBAC roles
"""

from oslo_log import log as logging

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

from patrole_tempest_plugin import rbac_rule_validation

from tempest import config
from tempest.lib import decorators
from tempest.lib.common.utils import data_utils
from tempest.lib.decorators import idempotent_id

CONF = config.CONF
LOG = logging.getLogger(__name__)


# noinspection PyPep8Naming
class VirtualDNSTest(rbac_base.BaseContrailTest):

    """
    Test class to test virtual dns objects using RBAC roles
    """

    def _create_virtual_dns(self):
        parent_type = "domain"
        virtual_dns_data = {"domain_name": "default-domain",
                            "default_ttl_seconds": 0,
                            "record_order": "fixed"}
        display_name = data_utils.rand_name('virtual-dns')
        fq_name = ["default-domain", display_name]
        dns = self.virtual_dns_client.create_virtual_dns(
            parent_type=parent_type,
            virtual_DNS_data=virtual_dns_data,
            display_name=display_name,
            fq_name=fq_name)
        self.addCleanup(self._try_delete_resource,
                        self.virtual_dns_client.delete_virtual_dns,
                        dns['virtual-DNS']['uuid'])
        return dns

    def _create_virtual_dns_record(self, dns):
        parent_type = "virtual-DNS"
        record_name = data_utils.rand_name('virtual-dns-record')
        virtual_dns_record_data = {"record_type": "A",
                                   "record_ttl_seconds": 86400,
                                   "record_name": record_name,
                                   "record_class": "IN",
                                   "record_data": "1.1.1.1"}
        fq_name = dns['virtual-DNS']['fq_name']
        fq_name.append(record_name)
        parent_uuid = dns['virtual-DNS']['uuid']
        dns_record = self.virtual_dns_client.create_virtual_dns_records(
            parent_type=parent_type,
            virtual_DNS_record_data=virtual_dns_record_data,
            fq_name=fq_name,
            parent_uuid=parent_uuid)
        self.addCleanup(self._try_delete_resource,
                        self.virtual_dns_client.delete_virtual_dns_record,
                        dns_record['virtual-DNS-record']['uuid'])
        return dns_record

    @decorators.idempotent_id('0efa3a9e-42da-4cfe-ae7f-c216220cc3a8')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_virtual_DNSs")
    @idempotent_id('8401d690-afdf-4b6e-ad60-b9363a8cfb1d')
    def test_list_virtual_dns(self):
        """
        test method for list virtual dns objects
        """
        with self.rbac_utils.override_role(self):
            self.virtual_dns_client.list_virtual_dns()

    @decorators.idempotent_id('92221008-5ccf-4f04-ac9a-64082bf6d545')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_virtual_DNSs")
    @idempotent_id('a7dd2c9e-e1eb-4dc4-ac70-4d48a291a3bf')
    def test_create_virtual_dns(self):
        """
        test method for create virtual dns objects
        """
        with self.rbac_utils.override_role(self):
            self._create_virtual_dns()

    @decorators.idempotent_id('3581ee83-498c-4d57-b0b4-079a6e197b00')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_virtual_DNS")
    @idempotent_id('ffc0fc82-3bff-48ab-b65a-3d90b4a3154d')
    def test_show_virtual_dns(self):
        """
        test method for show virtual dns objects
        """
        dns = self._create_virtual_dns()
        with self.rbac_utils.override_role(self):
            self.virtual_dns_client.show_virtual_dns(
                dns['virtual-DNS']['uuid'])

    @decorators.idempotent_id('e96aa8ba-4ece-4aed-b644-9dd120bfebba')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_virtual_DNS")
    @idempotent_id('4793caa1-7707-4123-b1b4-c3feae91312f')
    def test_delete_virtual_dns(self):
        """
        test method for delete virtual dns objects
        """
        dns = self._create_virtual_dns()
        with self.rbac_utils.override_role(self):
            self.virtual_dns_client.delete_virtual_dns(
                dns['virtual-DNS']['uuid'])

    @decorators.idempotent_id('30abbf69-f415-42a7-b48e-05dd04d86054')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_virtual_DNS")
    @idempotent_id('2bc43935-57c1-4bf6-9868-78ccfce164bb')
    def test_update_virtual_dns(self):
        """
        test method for update virtual dns objects
        """
        dns = self._create_virtual_dns()
        virtual_dns_data = {"domain_name": "default-domain",
                            "default_ttl_seconds": 0,
                            "record_order": "fixed"}
        display_name = data_utils.rand_name('virtual-dns-updated')
        with self.rbac_utils.override_role(self):
            self.virtual_dns_client.update_virtual_dns(
                dns_id=dns['virtual-DNS']['uuid'],
                virtual_DNS_data=virtual_dns_data,
                display_name=display_name)

    @decorators.idempotent_id('dc10131d-d432-4251-bc95-dae08f0fd865')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_virtual_DNS_records")
    @idempotent_id('e9103999-2f02-4f04-a8a0-906ca4fb394d')
    def test_list_virtual_dns_records(self):
        """
        test method for list virtual dns record objects
        """
        with self.rbac_utils.override_role(self):
            self.virtual_dns_client.list_virtual_dns_records()

    @decorators.idempotent_id('60923321-d8d7-442e-8a8f-97a0669a9440')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_virtual_DNS_records")
    @idempotent_id('bd9f3992-0ce4-4477-97a0-1271bc8ad9ef')
    def test_create_virtual_dns_records(self):
        """
        test method for create virtual dns record objects
        """
        # A virtual DNS is needed to create a record
        dns = self._create_virtual_dns()
        with self.rbac_utils.override_role(self):
            self._create_virtual_dns_record(dns)

    @decorators.idempotent_id('53b57fa1-6834-42ae-8e5d-b4059bfdc533')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_virtual_DNS_record")
    @idempotent_id('fa3d1a2b-d788-4623-89a4-3a9ed1db7a7d')
    def test_show_virtual_dns_record(self):
        """
        test method for show virtual dns record objects
        """
        # A virtual DNS is needed to create a record
        dns = self._create_virtual_dns()
        dns_record = self._create_virtual_dns_record(dns)
        with self.rbac_utils.override_role(self):
            self.virtual_dns_client.show_virtual_dns_record(
                dns_record['virtual-DNS-record']['uuid'])

    @decorators.idempotent_id('51946356-0d9e-47a7-a6c2-748160ccd09a')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_virtual_DNS_record")
    @idempotent_id('de31e867-c997-4b4c-a095-43c647f5c192')
    def test_delete_virtual_dns_record(self):
        """
        test method for delete virtual dns record objects
        """
        # A virtual DNS is needed to create a record
        dns = self._create_virtual_dns()
        dns_record = self._create_virtual_dns_record(dns)
        with self.rbac_utils.override_role(self):
            self.virtual_dns_client.delete_virtual_dns_record(
                dns_record['virtual-DNS-record']['uuid'])

    @decorators.idempotent_id('0b5e0c65-b494-4cd0-9c6b-31871afd0459')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_virtual_DNS_record")
    @idempotent_id('65acef26-646f-4b36-923c-8a1d07e90c5c')
    def test_update_virtual_dns_record(self):
        """
        test method for update virtual dns record objects
        """
        # A virtual DNS is needed to create a record
        dns = self._create_virtual_dns()
        dns_record = self._create_virtual_dns_record(dns)
        record_name = data_utils.rand_name('virtual-dns-record-updated')
        virtual_dns_record_data = {"record_type": "A",
                                   "record_ttl_seconds": 86400,
                                   "record_name": record_name,
                                   "record_class": "IN",
                                   "record_data": "1.1.1.1"}
        with self.rbac_utils.override_role(self):
            self.virtual_dns_client.update_virtual_dns_record(
                dns_record_id=dns_record['virtual-DNS-record']['uuid'],
                virtual_DNS_record_data=virtual_dns_record_data)
