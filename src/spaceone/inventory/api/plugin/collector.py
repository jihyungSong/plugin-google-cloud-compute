# -*- coding: utf-8 -*-

from spaceone.api.inventory.plugin import collector_pb2, collector_pb2_grpc
from spaceone.core.pygrpc import BaseAPI
from spaceone.core.pygrpc.message_type import *


class Collector(BaseAPI, collector_pb2_grpc.CollectorServicer):

    pb2 = collector_pb2
    pb2_grpc = collector_pb2_grpc

    def verify(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('CollectorService', metadata) as collector_svc:
            data = collector_svc.verify(params)
            return self.locator.get_info('CollectorVerifyInfo', data)

    def collect(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('CollectorService', metadata) as collector_svc:
            # response = ['i-1','i-2','i-3','i-4','i-5']
            resource = collector_svc.list_resources(params)
            for res in resource:

                res = {
                    'state': (res['state']),
                    'message': '',
                    'resource_type': (res['resource_type']),
                    'match_rules': change_struct_type(res['match_rules']),
                    'replace_rules': change_struct_type({}),
                    'resource': change_struct_type(res['resource'])
                }

                yield self.locator.get_info('ResourceInfo', res)
