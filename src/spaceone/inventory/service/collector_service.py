import time
import logging
import concurrent.futures

from spaceone.core.service import *
from spaceone.inventory.manager.collector_manager import CollectorManager

_LOGGER = logging.getLogger(__name__)

FILTER_FORMAT = [
    {
        'key': 'project_id',
        'name': 'Project ID',
        'type': 'str',
        'resource_type': 'SERVER',
        'search_key': 'identity.Project.project_id',
        'change_rules': [{
            'resource_key': 'data.compute.instance_id',
            'change_key': 'instance_id'
        }, {
            'resource_key': 'data.compute.region',
            'change_key': 'region_name'
        }]
    }, {
        'key': 'collection_info.service_accounts',
        'name': 'Service Account ID',
        'type': 'str',
        'resource_type': 'SERVER',
        'search_key': 'identity.ServiceAccount.service_account_id',
        'change_rules': [{
            'resource_key': 'data.compute.instance_id',
            'change_key': 'instance_id'
        }, {
            'resource_key': 'data.compute.region',
            'change_key': 'region_name'
        }]
    }, {
        'key': 'server_id',
        'name': 'Server ID',
        'type': 'list',
        'resource_type': 'SERVER',
        'search_key': 'inventory.Server.server_id',
        'change_rules': [{
            'resource_key': 'data.compute.instance_id',
            'change_key': 'instance_id'
        }, {
            'resource_key': 'data.compute.region',
            'change_key': 'region_name'
        }]
    }, {
        'key': 'instance_id',
        'name': 'Instance ID',
        'type': 'list',
        'resource_type': 'CUSTOM'
    },
    {
        'key': 'region_name',
        'name': 'Region',
        'type': 'list',
        'resource_type': 'CUSTOM'
    }
]

SUPPORTED_RESOURCE_TYPE = ['inventory.Server', 'inventory.Region']
NUMBER_OF_CONCURRENT = 50


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.collector_manager: CollectorManager = self.locator.get_manager('CollectorManager')

    @transaction
    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        capability = {
            'filter_format': FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE
            }
        return {'metadata': capability}

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """ verify options capability
        Args:
            params
              - options
              - secret_data: may be empty dictionary

        Returns:

        Raises:
             ERROR_VERIFY_FAILED:
        """
        manager = self.locator.get_manager('CollectorManager')
        secret_data = params['secret_data']
        options = params.get('options', {})
        active = manager.verify(options, secret_data)
        return {}

    @transaction
    @check_required(['options', 'secret_data', 'filter'])
    def list_resources(self, params):
        """ Get quick list of resources
        Args:
            params:
                - options
                - secret_data
                - filter

        Returns: list of resources
        """

        start_time = time.time()

        self.collector_manager.set_connector(params['secret_data'])

        print("---> List Regions Call")
        all_regions = self.collector_manager.list_regions(params['secret_data'])

        resource_regions = []
        collected_region_code = []

        server_resource_format = {'resource_type': 'inventory.Server',
                                  'match_rules': {'1': ['reference.resource_id']}}

        region_resource_format = {'resource_type': 'inventory.Region',
                                  'match_rules': {'1': ['region_code', 'region_type']}}

        print("---> AZ")
        target_zones = self.get_target_zones(params, all_regions)
        print("---> Connector")
        gcp_connectors = self.set_connectors(params, target_zones)
        params_with_zones = self.set_params_for_zones(params, target_zones, gcp_connectors)

        # TODO: parallel collecting instances through multi threading
        target_params = []
        is_instance = False

        instance_start_time = time.time()

        multi_params = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_CONCURRENT) as executor:
            future_executors = []
            for params_with_zone in params_with_zones:
                # future_executors.append(executor.submit(self.collector_manager.list_instances_only, mt_param))
                future_executors.append(executor.submit(self.set_params_for_instances, params_with_zone))

            for future in concurrent.futures.as_completed(future_executors):
                _params_with_instances = future.result()

                if _params_with_instances:
                    multi_params.append(_params_with_instances)
                    is_instance = True

        # for params in mt_params:
        #     print(f"---> List Instance Only Call: {params['zone_info']['zone']}")
        #     _instances = self.collector_manager.list_instances_only(params)
        #
        #     if _instances:
        #         params.update({
        #             'instances':  _instances
        #         })
        #
        #         target_params.append(params)
        #         is_instance = True

        print(f'instance FINISHED {time.time() - instance_start_time} Sec ##################')

        if is_instance:
            print('---> List Global Resources Call')
            global_resources = self.collector_manager.get_global_resources(params['secret_data'], all_regions,
                                                                           gcp_connectors)

            resources = []
            for params in multi_params:
                params.update({
                    'resources': global_resources
                })

                # resources.extend(self.collector_manager.list_resources(params))

            with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_CONCURRENT) as executor:
                future_executors = []
                for _params in multi_params:
                    future_executors.append(executor.submit(self.collector_manager.list_resources, _params))

                for future in concurrent.futures.as_completed(future_executors):
                    for result in future.result():
                        collected_region = self.collector_manager.get_region_from_result(result)

                        if collected_region is not None and collected_region.region_code not in collected_region_code:
                            resource_regions.append(collected_region)
                            collected_region_code.append(collected_region.region_code)

                        yield result, server_resource_format

            for resource_region in resource_regions:
                yield resource_region, region_resource_format

            for resource in resources:
                collected_region = self.collector_manager.get_region_from_result(resource)

                if collected_region and collected_region.region_code not in collected_region_code:
                    resource_regions.append(collected_region)
                    collected_region_code.append(collected_region.region_code)

                yield resource, server_resource_format

            for resource_region in resource_regions:
                yield resource_region, region_resource_format

        #
        # with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_CONCURRENT) as executor:
        #     future_executors = []
        #     for mt_param in mt_params:
        #         future_executors.append(executor.submit(self.collector_manager.list_resources, mt_param))
        #
        #     for future in concurrent.futures.as_completed(future_executors):
        #         for result in future.result():
        #             collected_region = self.collector_manager.get_region_from_result(result)
        #
        #             if collected_region is not None and collected_region.region_code not in collected_region_code:
        #                 resource_regions.append(collected_region)
        #                 collected_region_code.append(collected_region.region_code)
        #
        #             yield result, server_resource_format
        #
        # for resource_region in resource_regions:
        #     yield resource_region, region_resource_format

        print(f'############## TOTAL FINISHED {time.time() - start_time} Sec ##################')

    def get_target_zones(self, params, all_regions):
        query, instance_ids, filter_region_name = self._check_query(params['filter'])
        return self.get_all_zones(params.get('secret_data', ''), filter_region_name, all_regions)

    def set_connectors(self, params, zones):
        connectors = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_CONCURRENT) as executor:
            future_executors = []
            for zone in zones:
                future_executors.append(executor.submit(self.set_connector, params))

            for future in concurrent.futures.as_completed(future_executors):
                connectors.append(future.result())

        return connectors

    def set_connector(self, params):
        _conn = self.locator.get_connector('GoogleCloudComputeConnector')
        _conn.get_connect(params['secret_data'])
        return _conn

    def set_params_for_zones(self, params, target_zones, connectors):
        # print("[ SET Params for ZONES ]")
        params_for_zones = []

        query, instance_ids, filter_region_name = self._check_query(params['filter'])

        for i, target_zone in enumerate(target_zones):
            params_for_zones.append({
                'zone_info': target_zone,
                'query': query,
                'secret_data': params['secret_data'],
                'instance_ids': instance_ids,
                'connector': connectors[i]
            })

        return params_for_zones

    def set_params_for_instances(self, params):
        instances = self.collector_manager.list_instances_only(params)

        if instances:
            params.update({
                'instances': instances
            })

            return params

        return None

    def get_all_zones(self, secret_data, filter_region_name, all_regions):
        """ Find all zone name
        Args:
            secret_data: secret data
            filter_region_name (list): list of region_name if wanted

        Returns: list of zones
        """
        match_zones = []

        if 'region_name' in secret_data:
            match_zones = self.match_zones_from_region(all_regions, secret_data['region_name'])

        if len(filter_region_name) > 0:
            for _region in filter_region_name:
                match_zones = self.match_zones_from_region(all_regions, _region)

        if not match_zones:
            # print(f'region count = {len(all_regions)}')
            for region in all_regions:
                for zone in region.get('zones', []):
                    match_zones.append({'zone': self._get_zone_name_from_zone_uri(zone), 'region': region['name']})

        return match_zones

    @staticmethod
    def match_zones_from_region(all_regions, region):
        match_zones = []

        for _region in all_regions:
            if _region['name'] == region:
                for _zone in _region.get('zones', []):
                    match_zones.append({'region': region, 'zone': _zone.split('/')[-1]})

        return match_zones

    @staticmethod
    def get_full_resource_name(project_id, resource_type, resource):
        return f'https://www.googleapis.com/compute/v1/projects/{project_id}/{resource_type}/{resource}'

    @staticmethod
    def _check_query(query):
        """
        Args:
            query (dict): example
                  {
                      'instance_id': ['i-123', 'i-2222', ...]
                      'instance_type': 'm4.xlarge',
                      'region_name': ['aaaa']
                  }
        If there is regiona_name in query, this indicates searching only these regions
        """

        instance_ids = []
        filters = []
        region_name = []
        for key, value in query.items():
            if key == 'instance_id' and isinstance(value, list):
                instance_ids = value

            elif key == 'region_name' and isinstance(value, list):
                region_name.extend(value)

            else:
                if not isinstance(value, list):
                    value = [value]

                if len(value) > 0:
                    filters.append({'Name': key, 'Values': value})

        return filters, instance_ids, region_name

    @staticmethod
    def _get_zone_name_from_zone_uri(zone):
        return zone.split('/')[-1]
