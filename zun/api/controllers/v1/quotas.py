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

import pecan

from zun.api.controllers import base
from zun.api.controllers.v1.schemas import quotas as schema
from zun.api import validation
from zun.common import exception
from zun.common import policy
from zun.common import quota
from zun import objects

QUOTAS = quota.QUOTAS


class QuotaController(base.Controller):
    """Controller for Quotas"""

    _custom_actions = {
        'defaults': ['GET'],
    }

    def _get_quotas(self, context, usages=False):
        values = QUOTAS.get_project_quotas(context, context.project_id,
                                           usages=usages)

        if usages:
            return values
        else:
            return {k: v['limit'] for k, v in values.items()}

    @pecan.expose('json')
    @exception.wrap_pecan_controller_exception
    @validation.validate_query_param(pecan.request, schema.query_param_update)
    @validation.validated(schema.query_param_update)
    def put(self, **quotas_dict):
        context = pecan.request.context
        policy.enforce(context, 'quota:update',
                       action='quota:update')
        project_id = context.project_id
        for key, value in quotas_dict.items():
            value = int(value)
            quota = objects.Quota(context, project_id=project_id, resource=key,
                                  hard_limit=value)
            try:
                quota.create(context)
            except exception.QuotaExists:
                quota.update(context)
        return self._get_quotas(context)

    @pecan.expose('json')
    @exception.wrap_pecan_controller_exception
    def get(self, **kwargs):
        context = pecan.request.context
        usages = kwargs.get('usages', False)
        policy.enforce(context, 'quota:get',
                       action='quota:get')
        return self._get_quotas(context, usages=usages)

    @pecan.expose('json')
    @exception.wrap_pecan_controller_exception
    def defaults(self):
        context = pecan.request.context
        policy.enforce(context, 'quota:get_default',
                       action='quota:get_default')
        values = QUOTAS.get_defaults(context)
        return values

    @pecan.expose('json')
    @exception.wrap_pecan_controller_exception
    def delete(self):
        context = pecan.request.context
        policy.enforce(context, 'quota:delete',
                       action='quota:delete')
        QUOTAS.destroy_all_by_project(context, context.project_id)
