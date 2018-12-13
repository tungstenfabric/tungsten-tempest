# Copyright 2018 AT&T Corp
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

from oslo_serialization import jsonutils as json

from six.moves import urllib
from tempest.lib.common import rest_client as service_client

from tungsten_tempest_plugin.services.contrail.json import base


class ContrailClient(base.BaseContrailClient):
    """Generic client for Contrail API

    Client implements all basic CRUD functions for Contrail API.
    http://www.opencontrail.org/documentation/api/r5.0/contrail_openapi.html
    """

    def _pluralize(self, resource_name):
        """Contrail API ignores common rules for pluralization. For example:

        .. Fetch a specific firewall-policy
        .. GET /firewall-policy/{id}
        and
        .. List collection of firewall-policy
        .. GET /firewall-policys

        This method is created so if it will be ever changed we can update it
        in one place.
        """
        return resource_name + 's'

    def _underscore_to_dash(self, name):
        return name.replace("_", "-")

    def _build_uri(self, name, **kwargs):
        uri = "/%s" % self._underscore_to_dash(name)
        if kwargs:
            uri += '?' + urllib.parse.urlencode(kwargs, doseq=1)
        return uri

    def _lister(self, plural_name):
        def _list(**filters):
            uri = self._build_uri(plural_name, **filters)
            resp, body = self.get(uri)
            result = {plural_name: json.loads(body)}
            self.expected_success(200, resp.status)
            return service_client.ResponseBody(resp, result)

        return _list

    def _deleter(self, resource_name):
        def _delete(resource_id):
            uri = '%s/%s' % (resource_name, resource_id)
            uri = self._build_uri(uri)
            resp, body = self.delete(uri)
            self.expected_success(200, resp.status)
            return service_client.ResponseBody(resp, body)

        return _delete

    def _shower(self, resource_name):
        def _show(resource_id, **fields):
            uri = '%s/%s' % (resource_name, resource_id)
            uri = self._build_uri(uri)

            if fields:
                uri += '?' + urllib.parse.urlencode(fields, doseq=1)
            resp, body = self.get(uri)
            body = json.loads(body)
            self.expected_success(200, resp.status)
            return service_client.ResponseBody(resp, body)

        return _show

    def _creater(self, resource_name):
        def _create(**kwargs):
            uri = self._build_uri(self._pluralize(resource_name))
            post_data = json.dumps({
                self._underscore_to_dash(resource_name): kwargs})
            resp, body = self.post(uri, post_data)
            body = json.loads(body)
            self.expected_success(200, resp.status)
            return service_client.ResponseBody(resp, body)

        return _create

    def _updater(self, resource_name):
        def _update(res_id, **kwargs):
            uri = '%s/%s' % (resource_name, res_id)
            uri = self._build_uri(uri)
            put_data = json.dumps({
                self._underscore_to_dash(resource_name): kwargs})
            resp, body = self.put(uri, put_data)
            body = json.loads(body) if body else {}
            self.expected_success(200, resp.status)
            return service_client.ResponseBody(resp, body)

        return _update

    def __getattr__(self, name):
        """Client entry point

        Once user will call CRUD method it will be managed here.
        """
        method_prefixes = ["list_", "delete_", "show_", "create_", "update_"]
        method_functors = [self._lister,
                           self._deleter,
                           self._shower,
                           self._creater,
                           self._updater]
        for index, prefix in enumerate(method_prefixes):
            prefix_len = len(prefix)
            if name[:prefix_len] == prefix:
                return method_functors[index](name[prefix_len:])
        raise AttributeError(name)
