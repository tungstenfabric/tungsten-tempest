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
Base class for contrail testing against RBAC rules
"""

from oslo_log import log as logging
from patrole_tempest_plugin import rbac_utils
from tempest import config
from tempest.lib import exceptions
from tempest import test

from tungsten_tempest_plugin.services.contrail.json.access_control_client \
    import AccessControlClient
from tungsten_tempest_plugin.services.contrail.json.alarm_client \
    import AlarmClient
from tungsten_tempest_plugin.services.contrail.json.alias_ip_client \
    import AliasIPsClient
from tungsten_tempest_plugin.services.contrail.json.analytics_node_client \
    import AnalyticsNodeClient
from tungsten_tempest_plugin.services.contrail.json.\
    attachments_client import AttachmentsClient
from tungsten_tempest_plugin.services.contrail.json.bgp_as_a_service_client \
    import BGPAsAServiceClient
from tungsten_tempest_plugin.services.contrail.json.config_client import \
    ConfigClient
from tungsten_tempest_plugin.services.contrail.json.contrail_client import \
    ContrailClient
from tungsten_tempest_plugin.services.contrail.json.database_client import \
    ContrailDatabaseClient
from tungsten_tempest_plugin.services.contrail.json.\
    discovery_service_assignment_client import DiscoveryServiceAssignmentClient
from tungsten_tempest_plugin.services.contrail.json.domain_client import \
    DomainClient
from tungsten_tempest_plugin.services.contrail.json.dsa_rule_client \
    import DSARuleClient
from tungsten_tempest_plugin.services.contrail.json.floating_ip_client import \
    FloatingIpClient
from tungsten_tempest_plugin.services.contrail.json.forwarding_class_client \
    import ForwardingClassClient
from tungsten_tempest_plugin.services.contrail.json.fq_client import \
    FqnameIdClient
from tungsten_tempest_plugin.services.contrail.json.instance_ip_client import \
    InstanceIPClient
from tungsten_tempest_plugin.services.contrail.json.interface_client import \
    InterfaceClient
from tungsten_tempest_plugin.services.contrail.json.\
    load_balancer_client import LoadBalancerClient
from tungsten_tempest_plugin.services.contrail.json.namespace_client import \
    NamespaceClient
from tungsten_tempest_plugin.services.contrail.json.network_ipams_client \
    import NetworkIpamsClient
from tungsten_tempest_plugin.services.contrail.json.\
    network_policy_client import NetworkPolicyClient
from tungsten_tempest_plugin.services.contrail.json.port_tuple_client import \
    PortTupleClient
from tungsten_tempest_plugin.services.contrail.json.project_client import \
    ProjectClient
from tungsten_tempest_plugin.services.contrail.json.qos_client import \
    QosContrailClient
from tungsten_tempest_plugin.services.contrail.json.route_client \
    import RouteClient
from tungsten_tempest_plugin.services.contrail.json.router_client \
    import RouterClient
from tungsten_tempest_plugin.services.contrail.json.routing_client \
    import RoutingClient
from tungsten_tempest_plugin.services.contrail.json.\
    routing_policy_client import RoutingPolicyClient
from tungsten_tempest_plugin.services.contrail.json.security_group_client \
    import SecurityGroupClient
from tungsten_tempest_plugin.services.contrail.json.service_appliances_client \
    import ServiceAppliancesClient
from tungsten_tempest_plugin.services.contrail.json.service_client \
    import ServiceClient
from tungsten_tempest_plugin.services.contrail.json.subnet_client \
    import SubnetClient
from tungsten_tempest_plugin.services.contrail.json.virtual_dns_client import \
    VirtualDNSClient
from tungsten_tempest_plugin.services.contrail.json.\
    virtual_ip_client import VirtualIPClient
from tungsten_tempest_plugin.services.contrail.json.\
    virtual_network_client import VirtualNetworkClient
from tungsten_tempest_plugin.services.contrail.json.vm_contrail_client import \
    VmContrailClient

CONF = config.CONF
LOG = logging.getLogger(__name__)


def get_contail_version():
    return float(CONF.sdn.contrail_version)


class BaseContrailTest(rbac_utils.RbacUtilsMixin, test.BaseTestCase):
    """Base class for Contrail tests."""
    credentials = ['primary', 'admin']

    required_contrail_version = None

    @classmethod
    def skip_if_contrail_version_less(cls, version):
        if get_contail_version() < version:
            msg = "The tests require Contrail >= %s" % version
            raise cls.skipException(msg)

    @classmethod
    def skip_checks(cls):
        super(BaseContrailTest, cls).skip_checks()
        if not CONF.service_available.contrail:
            raise cls.skipException("Contrail support is required")
        if not CONF.patrole.enable_rbac:
            raise cls.skipException(
                "%s skipped as RBAC Flag not enabled" % cls.__name__)
        if CONF.auth.tempest_roles != ['admin']:
            raise cls.skipException(
                "%s skipped because tempest roles is not admin" % cls.__name__)
        if cls.required_contrail_version:
            cls.skip_if_contrail_version_less(cls.required_contrail_version)

    @classmethod
    def setup_clients(cls):
        super(BaseContrailTest, cls).setup_clients()
        cls.auth_provider = cls.os_primary.auth_provider
        cls.admin_client = cls.os_admin.networks_client
        dscv = CONF.identity.disable_ssl_certificate_validation
        ca_certs = CONF.identity.ca_certificates_file

        cls.access_control_client = AccessControlClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.alarm_client = AlarmClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.vm_client = VmContrailClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.dsa_client = DiscoveryServiceAssignmentClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.dsa_rule_client = DSARuleClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.forwarding_class_client = ForwardingClassClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.qos_client = QosContrailClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.routing_client = RoutingClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.security_group_client = SecurityGroupClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.service_appliances_client = ServiceAppliancesClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.analytics_node_client = AnalyticsNodeClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.vn_client = VirtualNetworkClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.db_client = ContrailDatabaseClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.fip_client = FloatingIpClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.fq_client = FqnameIdClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.virtual_ip_client = VirtualIPClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.virtual_dns_client = VirtualDNSClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.domain_client = DomainClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.project_client = ProjectClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.port_tuple_client = PortTupleClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.network_policy_client = NetworkPolicyClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.routing_policy_client = RoutingPolicyClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.namespace_client = NamespaceClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.network_ipams_client = NetworkIpamsClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.bgp_as_a_service_client = BGPAsAServiceClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.iip_client = InstanceIPClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.subnet_client = SubnetClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.load_balancer_client = LoadBalancerClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.route_client = RouteClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.interface_client = InterfaceClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.router_client = RouterClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.service_client = ServiceClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.attachments_client = AttachmentsClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.config_client = ConfigClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.alias_ip_client = AliasIPsClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)
        cls.contrail_client = ContrailClient(
            cls.auth_provider,
            CONF.sdn.catalog_type,
            CONF.identity.region,
            CONF.sdn.endpoint_type,
            disable_ssl_certificate_validation=dscv,
            ca_certs=ca_certs)

    @classmethod
    def resource_setup(cls):
        cls.tenant_name = cls.os_primary.credentials.tenant_name

    @classmethod
    def _try_delete_resource(cls, delete_callable, *args, **kwargs):
        """Cleanup resources in case of test-failure

        Some resources are explicitly deleted by the test.
        If the test failed to delete a resource, this method will execute
        the appropriate delete methods. Otherwise, the method ignores NotFound
        exceptions thrown for resources that were correctly deleted by the
        test.

        :param delete_callable: delete method
        :param args: arguments for delete method
        :param kwargs: keyword arguments for delete method
        """
        try:
            delete_callable(*args, **kwargs)
        # if resource is not found, this means it was deleted in the test
        except exceptions.NotFound:
            pass
