# -*- coding: utf-8 -*-

__all__ = ['CollectorManager']

import logging

from spaceone.core import config
from spaceone.core.error import *
from spaceone.core.manager import BaseManager

_LOGGER = logging.getLogger(__name__)


class CollectorManager(BaseManager):
    def __init__(self, transaction):
        super().__init__(transaction)

    ###################
    # Verify
    ###################
    def verify(self, options, credentials={}):
        """ Check Google OAuth connection

        Args:
            options:
              - client_id
        """
        connector = self.locator.get_connector('GcpComputeConnector')
        r = connector.verify(options, credentials)
        # ACTIVE/UNKNOWN
        return r

    def list_resources(self, options, credentials, filter):


        connector = self.locator.get_connector('GcpComputeConnector')
        connector.verify(options, credentials)

        # make query, based on options, credentials, filter
        query = {}

        #
        region_id = None
        zone_id = None
        pool_id = None
        project_id = None

        if 'region_id' in credentials:
            region_id = credentials['region_id']
        if 'zone_id' in credentials:
            zone_id = credentials['zone_id']
        if 'pool_id' in credentials:
            pool_id = credentials['pool_id']
        if 'identity.project_id' in credentials:
            project_id = credentials['identity.project_id']


        return connector.collectInfo(query, region_id, zone_id, pool_id, project_id)
