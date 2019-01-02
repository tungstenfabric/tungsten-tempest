"""Tempest Suite for Contrail BGP_VPN."""
# Copyright 2018 AT&T Intellectual Property.
# All other rights reserved.
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

from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF


class BgpvpnTest(rbac_base.BaseContrailTest):
    """Test suite for validating RBAC functionality of 'bgpvpn' API."""

    @classmethod
    def skip_checks(cls):
        super(BgpvpnTest, cls).skip_checks()
        if float(CONF.sdn.contrail_version) < 4:
            msg = "bgpvpn requires Contrail >= 4"
            raise cls.skipException(msg)

    @classmethod
    def resource_setup(cls):
        """Create Bgpvpn to use across the Suite."""
        super(BgpvpnTest, cls).resource_setup()
        cls.bgpvpn_uuid = cls._create_bgpvpn()

    @classmethod
    def _create_bgpvpn(cls):
        """Create Bgpvpn."""
        bgpvpn_name = data_utils.rand_name('test-bgpvpn')
        bgpvpn_fq_name = ['default-domain', cls.tenant_name, bgpvpn_name]
        resp_body = cls.contrail_client.create_bgpvpn(
            parent_type='project',
            fq_name=bgpvpn_fq_name)
        bgpvpn_uuid = resp_body['bgpvpn']['uuid']
        cls.addClassResourceCleanup(
            cls._try_delete_resource,
            cls.contrail_client.delete_bgpvpn,
            bgpvpn_uuid)
        return bgpvpn_uuid

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_bgpvpns"])
    @decorators.idempotent_id('65afb5d5-52cb-484c-9e8e-42509be7dd77')
    def test_list_bgpvpns(self):
        """Test whether current role can list of bgpvpns."""
        with self.rbac_utils.override_role(self):
            self.contrail_client.list_bgpvpns()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_bgpvpns"])
    @decorators.idempotent_id('c3a7510c-c8d6-4736-9962-5c1aa032bf79')
    def test_create_bgpvpns(self):
        """Test whether current role can create bgpvpn."""
        with self.rbac_utils.override_role(self):
            self._create_bgpvpn()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_bgpvpn"])
    @decorators.idempotent_id('2fd05ca2-97d8-477c-aead-a881a2ba5e7e')
    def test_show_bgpvpn(self):
        """Test whether current role can get bgpvpn details."""
        with self.rbac_utils.override_role(self):
            self.contrail_client.show_bgpvpn(
                self.bgpvpn_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_bgpvpn"])
    @decorators.idempotent_id('919aa2bb-1556-4dcf-bbef-0a31f9c6464b')
    def test_delete_bgpvpn(self):
        """Test whether current role can delete bgpvpn details."""
        new_bgpvpn_uuid = self._create_bgpvpn()
        with self.rbac_utils.override_role(self):
            self.contrail_client.delete_bgpvpn(
                new_bgpvpn_uuid)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_bgpvpn"])
    @decorators.idempotent_id('ae734791-eaeb-4ca9-908a-59d0eac1a3c0')
    def test_update_bgpvpn(self):
        """Test whether current role can update bgpvpn."""
        with self.rbac_utils.override_role(self):
            self.contrail_client.update_bgpvpn(
                self.bgpvpn_uuid,
                display_name=data_utils.rand_name('test-bgpvpn'))
