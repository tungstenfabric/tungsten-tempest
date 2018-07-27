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
Tempest service class for database service assignment test cases
"""

import json
from six.moves.urllib import parse as urllib
from tungsten_tempest_plugin.services.contrail.json import base


class DiscoveryServiceAssignmentClient(base.BaseContrailClient):

    """
    Service class for dsa test cases
    """

    def list_ds_assignments(self, params=None):
        """
        :param params:
        :return: response object
        """
        url = '/discovery-service-assignments'
        if params:
            url += '?%s' % urllib.urlencode(params)
        return self.get(url)

    def create_ds_assignments(self, **kwargs):
        """
        :param kwargs:
        :return: map object
        """
        url = '/discovery-service-assignments'
        post_body = json.dumps({'discovery-service-assignment': kwargs})
        resp, body = self.post(url, post_body)
        body = json.loads(body)
        return base.ResponseBody(resp, body)

    def show_ds_assignment(self, assignment_id):
        """
        :param assignment_id:
        :return: response object
        """
        url = '/discovery-service-assignment/%s' % str(assignment_id)
        return self.get(url)

    def delete_ds_assignment(self, assignment_id):
        """
        :param assignment_id:
        :return: response object
        """
        url = '/discovery-service-assignment/%s' % str(assignment_id)
        return self.delete(url)

    def update_ds_assignment(self, assignment_id, **kwargs):
        """
        :param assignment_id:
        :param kwargs:
        :return: map object
        """
        url = '/discovery-service-assignment/%s' % str(assignment_id)
        post_data = {'discovery-service-assignment': kwargs}
        req_post_data = json.dumps(post_data)
        resp, body = self.put(url, req_post_data)
        body = json.loads(body)
        return base.ResponseBody(resp, body)
