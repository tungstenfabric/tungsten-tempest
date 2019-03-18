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
Tempest test-case to test fqname ID objects using RBAC roles
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_rule_validation
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

CONF = config.CONF
LOG = logging.getLogger(__name__)


class FqnameIdTest(rbac_base.BaseContrailTest):
    """Test class to test Fqname ID objects using RBAC roles"""

    @classmethod
    def resource_setup(cls):
        super(FqnameIdTest, cls).resource_setup()
        # Create network to test fqname and uuid conversion
        net_name = data_utils.rand_name('rbac-fq-network')
        fq_name = ['default-domain', cls.tenant_name, net_name]
        post_body = {'parent_type': 'project', 'fq_name': fq_name}
        body = cls.vn_client.create_virtual_networks(**post_body)
        cls.network = body['virtual-network']
        cls.type = 'virtual-network'

    @classmethod
    def resource_cleanup(cls):
        cls._try_delete_resource(cls.vn_client.delete_virtual_network,
                                 cls.network['uuid'])
        super(FqnameIdTest, cls).resource_cleanup()

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["fqname_to_id"])
    @decorators.idempotent_id('1fc1350b-3146-49bc-9af5-a61a98b55541')
    def test_fqname_to_id(self):
        """test method for fqname to id rules objects"""
        with self.override_role():
            self.fq_client.fqname_to_id(fq_name=self.network['fq_name'],
                                        type=self.type)

    @rbac_rule_validation.action(service="Contrail",
                                 rules=["id_to_fqname"])
    @decorators.idempotent_id('ecdd77d7-8508-4639-86cd-b97907b363ff')
    def test_id_to_fqname(self):
        """test method for id to fqname rules objects"""
        with self.override_role():
            self.fq_client.id_to_fqname(uuid=self.network['uuid'])
