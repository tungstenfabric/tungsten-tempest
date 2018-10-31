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
Tempest test-case to test route objects using RBAC roles
"""

import random

from oslo_log import log as logging

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

from patrole_tempest_plugin import rbac_rule_validation

from tempest import config
from tempest.lib import decorators
from tempest.lib.common.utils import data_utils
from tempest.lib.decorators import idempotent_id

CONF = config.CONF
LOG = logging.getLogger(__name__)


class ContrailRouteTableTest(rbac_base.BaseContrailTest):

    """
    Test class to test route objects using RBAC roles
    """

    def _delete_route_table(self, route_id):
        self.route_client.delete_route_table(route_id)

    def _create_route_tables(self):
        parent_type = 'project'
        fq_name = ['default-domain', self.tenant_name,
                   data_utils.rand_name('Route')]
        route_table = self.route_client.create_route_tables(
            fq_name=fq_name,
            parent_type=parent_type)['route-table']
        self.addCleanup(self._try_delete_resource,
                        self._delete_route_table,
                        route_table['uuid'])
        return route_table

    @decorators.idempotent_id('600d0839-6c13-4349-9143-90f09bab41d3')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_route_tables")
    @idempotent_id('ca5a5d42-6e49-40e4-a5ac-de07b397b775')
    def test_list_route_tables(self):
        """
        test method for list route table objects
        """
        self._create_route_tables()
        with self.rbac_utils.override_role(self):
            self.route_client.list_route_tables()

    @decorators.idempotent_id('fa119fbf-9078-4607-9c85-344db9e2cf25')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_route_table")
    @idempotent_id('084a2759-991a-4ae2-bde4-8f9915966f6e')
    def test_show_route_table(self):
        """
        test method for show route table objects
        """
        route_table = self._create_route_tables()
        with self.rbac_utils.override_role(self):
            self.route_client.show_route_table(route_table['uuid'])

    @decorators.idempotent_id('6f8a79fd-593f-4558-9a43-ddd4781e8e4f')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_route_tables")
    @idempotent_id('3fab8105-c0be-4c9e-be5f-d2dce4deb921')
    def test_create_route_tables(self):
        """
        test method for create route table objects
        """
        with self.rbac_utils.override_role(self):
            self._create_route_tables()

    @decorators.idempotent_id('16c9ff63-26ba-4f4d-aa10-552555753cb5')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_route_table")
    @idempotent_id('2acee7ad-843e-40b0-b8f8-a6d90a51c6c8')
    def test_update_route_table(self):
        """
        test method for update route table objects
        """
        route_table = self._create_route_tables()
        display_name = data_utils.rand_name('RouteNew')
        with self.rbac_utils.override_role(self):
            self.route_client.update_route_table(
                route_id=route_table['uuid'],
                display_name=display_name)

    @decorators.idempotent_id('cedccde1-4509-4fe2-a7fb-5e6fcf32c10d')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_route_table")
    @idempotent_id('20a5086c-ec9a-43e0-ae2c-4161c0f4b280')
    def test_delete_route_table(self):
        """
        test method for delete route table objects
        """
        route_table = self._create_route_tables()
        with self.rbac_utils.override_role(self):
            self._delete_route_table(route_table['uuid'])


class ContrailInterfaceRouteTableTest(rbac_base.BaseContrailTest):

    """
    Test class to test route interface table using RBAC roles
    """

    def _delete_interface_route_table(self, route_id):
        self.route_client.delete_interface_route_table(route_id)

    def _create_interface_route_tables(self):
        parent_type = 'project'
        fq_name = ['default-domain',
                   self.tenant_name,
                   data_utils.rand_name('InterfaceRoute')]
        interface_route_table = self.route_client \
            .create_interface_route_tables(
                fq_name=fq_name,
                parent_type=parent_type)['interface-route-table']
        self.addCleanup(self._try_delete_resource,
                        self._delete_interface_route_table,
                        interface_route_table['uuid'])
        return interface_route_table

    @decorators.idempotent_id('6d34cf27-8a37-4d96-8420-f5d6013c0d84')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_interface_route_tables")
    @idempotent_id('b1f8f0a6-6074-4615-a439-19869a48bc49')
    def test_list_interface_route(self):
        """
        test method for list route interface table objects
        """
        self._create_interface_route_tables()
        with self.rbac_utils.override_role(self):
            self.route_client.list_interface_route_tables()

    @decorators.idempotent_id('f1c4cbd9-06e7-4ab2-a5d8-0cd4d50b03ea')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_interface_route_table")
    @idempotent_id('94703a28-5e33-4003-b95b-6a3cc5752fd4')
    def test_show_interface_route(self):
        """
        test method for show route interface table objects
        """
        interface_rte_table = self._create_interface_route_tables()
        with self.rbac_utils.override_role(self):
            self.route_client.show_interface_route_table(
                interface_rte_table['uuid'])

    @decorators.idempotent_id('e2f673d0-d631-4829-957e-d3f68653e948')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_interface_route_tables")
    @idempotent_id('b89ef437-4759-4c04-948b-d2ff9675ab07')
    def test_create_interface_route(self):
        """
        test method for create route interface table objects
        """
        with self.rbac_utils.override_role(self):
            self._create_interface_route_tables()

    @decorators.idempotent_id('29893eed-ecd5-489c-bc6f-0540aaea5188')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_interface_route_table")
    @idempotent_id('e9346d4f-7a07-41bc-8e88-e8ae9fa309ea')
    def test_update_interface_route(self):
        """
        test method for update route interface table objects
        """
        interface_rte_table = self._create_interface_route_tables()
        display_name = data_utils.rand_name('InterfaceRouteNew')
        with self.rbac_utils.override_role(self):
            self.route_client.update_interface_route_table(
                interface_route_id=interface_rte_table['uuid'],
                display_name=display_name)

    @decorators.idempotent_id('e50fec3c-4232-4df3-8965-e1cabd28f1ff')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_interface_route_table")
    @idempotent_id('b00444a5-cb4c-45bc-b393-503e9e333e98')
    def test_delete_interface_route(self):
        """
        test method for delete route interface table objects
        """
        interface_rte_table = self._create_interface_route_tables()
        with self.rbac_utils.override_role(self):
            self._delete_interface_route_table(
                interface_rte_table['uuid'])


class ContrailRouteTargetsTest(rbac_base.BaseContrailTest):

    """
    Test class to test route targets using RBAC roles
    """

    def _delete_route_target(self, target_id):
        self.route_client.delete_route_target(target_id)

    def _create_route_targets(self):
        # Contrail have changed way they parse fq_name for route-target.
        # Details: Route target must be of the format 'target:<asn>:<number>'
        # or 'target:<ip>:<number>'
        rand_name = "target:%s:%s" % (random.randint(10000, 99000),
                                      random.randint(10000, 99000))
        fq_name = [rand_name]
        route_target = self.route_client.create_route_targets(
            fq_name=fq_name)['route-target']
        self.addCleanup(self._try_delete_resource,
                        self._delete_route_target,
                        route_target['uuid'])
        return route_target

    @decorators.idempotent_id('7929fdbc-f12d-43e0-9804-70f3f5e94aed')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_route_targets")
    @idempotent_id('757efd07-8027-4a16-887a-1e42f16b4140')
    def test_list_route_targets(self):
        """
        test method for list route target objects
        """
        self._create_route_targets()
        with self.rbac_utils.override_role(self):
            self.route_client.list_route_targets()

    @decorators.idempotent_id('b4414a4e-f782-498d-842a-bd55bbdc52d0')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_route_target")
    @idempotent_id('76c60d98-dd5e-453a-bf0e-7854f78a1a5e')
    def test_show_route_target(self):
        """
        test method for show route target objects
        """
        target = self._create_route_targets()
        with self.rbac_utils.override_role(self):
            self.route_client.show_route_target(target['uuid'])

    @decorators.idempotent_id('64af449d-3fd9-4157-91f5-633cf1faeaa2')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_route_targets")
    @idempotent_id('fcdb4ebc-b92d-49f2-88e9-68c93aec94be')
    def test_create_route_targets(self):
        """
        test method for create route target objects
        """
        with self.rbac_utils.override_role(self):
            self._create_route_targets()

    @decorators.idempotent_id('c4c0b64e-f6d1-4704-8db7-a584c43e4199')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_route_target")
    @idempotent_id('dd830a77-4bfe-4a8c-b4e9-08b6ef2af3be')
    def test_update_route_target(self):
        """
        test method for update route target objects
        """
        target = self._create_route_targets()
        display_name = data_utils.rand_name('RouteTargetNew')
        with self.rbac_utils.override_role(self):
            self.route_client.update_route_target(
                route_target_id=target['uuid'],
                display_name=display_name)

    @decorators.idempotent_id('9ea8843c-11d8-4ab1-a7c8-3488d06dcc5c')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_route_target")
    @idempotent_id('dfaa58f9-ec29-4d51-a475-870fac08908d')
    def test_delete_route_target(self):
        """
        test method for delete route target objects
        """
        target = self._create_route_targets()
        with self.rbac_utils.override_role(self):
            self._delete_route_target(target['uuid'])


class ContrailRouteAggregateTest(rbac_base.BaseContrailTest):

    """
    Test class to test route aggregate using RBAC roles
    """

    def _delete_route_aggregate(self, route_aggr_id):
        self.route_client.delete_route_aggregate(route_aggr_id)

    def _create_route_aggregates(self):
        parent_type = 'project'
        fq_name = ['default-domain',
                   self.tenant_name,
                   data_utils.rand_name('RouteAggregate')]
        route_aggr = self.route_client.create_route_aggregates(
            fq_name=fq_name,
            parent_type=parent_type)['route-aggregate']
        self.addCleanup(self._try_delete_resource,
                        self._delete_route_aggregate,
                        route_aggr['uuid'])
        return route_aggr

    @decorators.idempotent_id('457b2f2d-a614-42be-8d07-595d684cdd6e')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="list_route_aggregates")
    @idempotent_id('15f2c30c-4404-4228-94a0-86c5ec5cf62e')
    def test_list_route_aggregates(self):
        """
        test method for list route aggregate objects
        """
        self._create_route_aggregates()
        with self.rbac_utils.override_role(self):
            self.route_client.list_route_aggregates()

    @decorators.idempotent_id('eb0990e2-ffca-4d19-947c-9a4476c9a3bc')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="show_route_aggregate")
    @idempotent_id('c8edee30-81c4-44e2-8485-055bed853384')
    def test_show_route_aggregate(self):
        """
        test method for show route aggregate objects
        """
        route_aggr = self._create_route_aggregates()
        with self.rbac_utils.override_role(self):
            self.route_client.show_route_aggregate(
                route_aggr['uuid'])

    @decorators.idempotent_id('c496716c-6674-41c0-a18a-a8eb8decd86b')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="create_route_aggregates")
    @idempotent_id('7553a54f-e41c-4555-b745-a858c5a70690')
    def test_create_route_aggregates(self):
        """
        test method for create route aggregate objects
        """
        with self.rbac_utils.override_role(self):
            self._create_route_aggregates()

    @decorators.idempotent_id('2dc40190-1d1b-4ee3-ad1c-5930d532481f')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="update_route_aggregate")
    @idempotent_id('de1e6102-0bc6-4f9b-a354-48eb051ab5e4')
    def test_update_route_aggregate(self):
        """
        test method for update route aggregate objects
        """
        route_aggr = self._create_route_aggregates()
        display_name = data_utils.rand_name('RouteAggregateNew')
        with self.rbac_utils.override_role(self):
            self.route_client.update_route_aggregate(
                route_aggr_id=route_aggr['uuid'],
                display_name=display_name)

    @decorators.idempotent_id('ee17d0db-7388-4428-9212-bbc4f4af07f9')
    @rbac_rule_validation.action(service="Contrail",
                                 rules="delete_route_aggregate")
    @idempotent_id('e16dbdc6-d7cf-43c7-af9d-bd76cc220200')
    def test_delete_route_aggregate(self):
        """
        test method for delete route aggregate objects
        """
        # Create aggregate
        route_aggr = self._create_route_aggregates()
        with self.rbac_utils.override_role(self):
            self._delete_route_aggregate(route_aggr['uuid'])
