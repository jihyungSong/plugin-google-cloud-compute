# -*- coding: utf-8 -*-

import logging


from spaceone.core.error import *
from spaceone.core.service import *

from spaceone.inventory.error import *

from spaceone.core.pygrpc.message_type import *

from spaceone.inventory.manager.collector_manager import CollectorManager

_LOGGER = logging.getLogger(__name__)

FILTER_FORMAT = [
{'key':'region_id', 'name':'Region', 'type':'str', 'resource_type': 'SERVER', 'change_key': ['data.compute.instance_id', 'instance_id']},
{'key':'zone_id', 'name':'Zone', 'type':'str', 'resource_type': 'SERVER', 'change_key': ['data.compute.instance_id', 'instance_id']},
{'key':'pool_id', 'name':'Pool', 'type':'str', 'resource_type': 'SERVER', 'change_key': ['data.compute.instance_id', 'instance_id']},
{'key':'server_id', 'name':'Server', 'type':'list', 'resource_type': 'SERVER', 'object_key': 'uuid', 'change_key': ['data.compute.instance_id', 'instance_id']},
{'key':'instance_id', 'name':'Instance ID', 'type':'list', 'resource_type': 'CUSTOM'},
{'key':'resource_type', 'name':'Resource Type', 'type':'str', 'enums': ['NETWORK', 'SUBNET', 'IP_ADDRESS'], 'resource_type': 'CUSTOM'},
]

SUPPORTED_RESOURCE_TYPE = ['SERVER']

@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

    @transaction
    @check_required(['options','credentials'])
    def verify(self, params):
        """ verify options capability
        Args:
            params
              - options
              - credentials: may be empty dictionary

        Returns:

        Raises:
            ERROR_NOT_FOUND: 
        """
        manager = self.locator.get_manager('CollectorManager')
        options = params['options']
        credentials = params['credentials']
        active = manager.verify(options, credentials)
        _LOGGER.debug(active)
        capability = {
            'filter_format':FILTER_FORMAT,
            'supported_resource_type' : SUPPORTED_RESOURCE_TYPE
            }
        return {'options': capability}

    @transaction
    @check_required(['options','credentials', 'filter'])
    def list_resources(self, params):
        """ Get quick list of resources
        
        Args:
            params:
                - options
                - credentials
                - filter

        Returns: list of resources
        """
        manager = self.locator.get_manager('CollectorManager')
        options = params['options']
        credentials = params['credentials']
        filter = params['filter']
        result_list = manager.list_resources(options, credentials, filter)

        _LOGGER.debug(result_list)

        return result_list

