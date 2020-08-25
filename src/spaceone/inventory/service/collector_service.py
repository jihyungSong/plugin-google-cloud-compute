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
NUMBER_OF_CONCURRENT = 20


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
        # parameter setting for multi threading
        all_regions = self.collector_manager.list_regions(params['secret_data'])

        mt_params = self.set_params_for_zones(params)
        resource_regions = []
        collected_region_code = []

        server_resource_format = {'resource_type': 'inventory.Server',
                                  'match_rules': {'1': ['reference.resource_id']}}

        region_resource_format = {'resource_type': 'inventory.Region',
                                  'match_rules': {'1': ['region_code', 'region_type']}}


        url_maps, instance_type, vpc, firewall, image, instance_groups = \
            self.collector_manager.get_zone_independent_resources(params['secret_data'], all_regions)

        with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_CONCURRENT) as executor:
            future_executors = []
            for mt_param in mt_params:
                future_executors.append(executor.submit(self.collector_manager.list_resources, mt_param))

            for future in concurrent.futures.as_completed(future_executors):
                for result in future.result():
                    collected_region = self.collector_manager.get_region_from_result(result)

                    if collected_region is not None and collected_region.region_code not in collected_region_code:
                        resource_regions.append(collected_region)
                        collected_region_code.append(collected_region.region_code)

                    yield result, server_resource_format

        for resource_region in resource_regions:
            yield resource_region, region_resource_format

        print(f'############## TOTAL FINISHED {time.time() - start_time} Sec ##################')

    def set_params_for_zones(self, params):
        params_for_zones = []

        (query, instance_ids, filter_region_name) = self._check_query(params['filter'])
        target_zones = self.get_all_zones(params.get('secret_data', ''), filter_region_name)

        for target_zone in target_zones:
            params_for_zones.append({
                'zone': target_zone,
                'query': query,
                'secret_data': params['secret_data'],
                'instance_ids': instance_ids
            })

        return params_for_zones

    def get_all_zones(self, secret_data, filter_region_name):
        """ Find all zone name
        Args:
            secret_data: secret data
            filter_region_name (list): list of region_name if wanted

        Returns: list of zones
        """
        match_zones = []
        zones = self.collector_manager.list_zones(secret_data)

        if 'region_name' in secret_data:
            match_zones = self.match_zones_from_region(zones, secret_data['regioni_name'],
                                                       self.get_full_resource_name(secret_data['project_id'],
                                                                                   'regions',
                                                                                   secret_data['region_name']))

        if len(filter_region_name) > 0:
            for _region in filter_region_name:
                match_zones = self.match_zones_from_region(zones, _region,
                                                           self.get_full_resource_name(secret_data['project_id'],
                                                                                       'regions', _region))

        if not match_zones:
            match_zones = list(map(lambda zone: {'zone': zone['name'], 'region': zone['region'].split('/')[-1]}, zones))

        return match_zones

    @staticmethod
    def match_zones_from_region(zones, region, full_region_resource):
        return [{'zone': zone['name'], 'region': region} for zone in zones if zone['region'] == full_region_resource]

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