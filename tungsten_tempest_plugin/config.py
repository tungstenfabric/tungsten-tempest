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
from oslo_config import cfg

service_available_group = cfg.OptGroup(name="service_available",
                                       title="Available OpenStack Services")

ServiceAvailableGroup = [
    cfg.BoolOpt("contrail",
                default=True,
                help="Whether or not contrail is expected to be available."),
]

sdn_group = cfg.OptGroup(name='sdn',
                         title='SDN service options')

SDNGroup = [
    cfg.StrOpt('endpoint_type',
               default='publicURL',
               choices=['public', 'admin', 'internal',
                        'publicURL', 'adminURL', 'internalURL'],
               help="The endpoint type to use for the SDN service"),
    cfg.StrOpt('catalog_type',
               default='sdn-l-config',
               help="Catalog type of the SDN service"),
]

tungsten_log_group = cfg.OptGroup(
    name='tungsten_log', title='tungsten Tempest Logging Options')

TungstenLogGroup = [
    cfg.BoolOpt('enable_reporting',
                default=False,
                help="Enables reporting on RBAC expected and actual test "
                     "results for each tungstenTempest test"),
    cfg.StrOpt('report_log_name',
               default='tungsten.log',
               help="Name of file where output from 'enable_reporting' is "
                    "logged. Note that this file is recreated on each "
                    "invocation of tungsten_tempest"),
    cfg.StrOpt('report_log_path',
               default='.',
               help="Path (relative or absolute) where the output from "
                    "'enable_reporting' is logged. This is combined with"
                    "report_log_name to generate the full path."),
]


def list_opts():
    """Return a list of oslo.config options available.

    The purpose of this is to allow tools like the Oslo sample config file
    generator to discover the options exposed to users.
    """
    opt_list = [
        (service_available_group, ServiceAvailableGroup),
        (sdn_group, SDNGroup),
        (tungsten_log_group, TungstenLogGroup)

    ]
    return opt_list
