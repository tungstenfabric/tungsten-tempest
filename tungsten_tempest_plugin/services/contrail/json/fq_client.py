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
Tempest service class for forward class test cases
"""

from oslo_serialization import jsonutils as json
from tungsten_tempest_plugin.services.contrail.json import base


class FqnameIdClient(base.BaseContrailClient):

    """
    Service class for fq name test cases
    """

    def fqname_to_id(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        uri = '/fqname-to-id'
        req_post_data = json.dumps(kwargs)

        resp, body = self.post(uri, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def id_to_fqname(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        uri = '/id-to-fqname'
        req_post_data = json.dumps(kwargs)

        resp, body = self.post(uri, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
