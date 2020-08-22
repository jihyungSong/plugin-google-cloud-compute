__all__ = ["VMConnector"]

import logging
import os
import itertools
import re
import google.oauth2.service_account
import googleapiclient
import googleapiclient.discovery
from pprint import pprint
from spaceone.core.connector import BaseConnector
from spaceone.core.utils import deep_merge
from collections import defaultdict

nested_dict = lambda: defaultdict(nested_dict)


def ddict2dict(d):
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = ddict2dict(v)
    return dict(d)


_LOGGER = logging.getLogger(__name__)

DATA_INFO = {
    'VM': {
        'resource_type': 'SERVER',
        'MATCH_RULES': {'1': ['data.compute.instance_id']},
    }
}

INSTANCE_TYPE_FILE = '%s/conf/%s' % (os.path.dirname(os.path.abspath(__file__)), 'instances.json')


class VMConnector(BaseConnector):

    def __init__(self, transaction=None, conf=None):
        self.client = None
        self.project_id = None
        self.region = None
        self.zone = None

    def verify(self, options, secret_data):
        self.get_connect(secret_data)
        return "ACTIVE"

    def get_connect(self, secret_data, service="compute_engine"):
        """
        cred(dict)
            - type: ..
            - project_id: ...
            - token_uri: ...
            - ...
        """
        try:
            credentials = google.oauth2.service_account.Credentials.from_service_account_info(secret_data)
            return googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
        except Exception as e:
            print(e)
            raise self.client(message='connection failed. Please check your authentication information.')

    def set_client(self, secret_data, zone_name):
        self.client = self.get_connect(secret_data)
        self.project_id = secret_data.get('project_id')
        self.region = self.get_region(zone_name)
        self.zone = zone_name

    def list_zones(self, secret_data):
        result = self.client.zones().list(project=secret_data.get('project_id')).execute()
        regions = result.get('items', [])
        return regions

    def list_instances(self, **query):
        status_filter = {'key': 'status', 'values': ['STAGING', 'RUNNING', 'STOPPING', 'REPAIRING']}

        if 'filter' in query:
            query.get('filter').append(status_filter)
        else:
            query.update({'filter': [status_filter]})

        query = self.generate_key_query('filter', self._get_filter_to_params(**query), '', is_default=True, **query)
        result = self.client.instances().list(**query).execute()
        compute_instances = result.get('items', [])
        return compute_instances, self.project_id

    def list_instance_types(self, **query):
        query = self.generate_query(is_default=True, **query)
        result = self.client.machineTypes().list(**query).execute()
        instance_types = result.get('items', [])
        return instance_types

    def list_url_maps(self, **query):
        response = self.client.urlMaps().list(project=self.project_id).execute()
        url_map = response.get('items', [])
        return url_map

    def list_vpc(self, **query):
        response = self.client.networks().list(project=self.project_id).execute()
        list_virtual_private_clouds = response.get('items', [])
        return list_virtual_private_clouds

    def list_subnet(self, **query):
        response = self.client.networks().list(project=self.project_id, region=self.region).execute()
        subnetworks = response.get('items', [])
        return subnetworks

    def list_disk(self, **query):
        response = self.client.disks().list(project=self.project_id, zone=self.zone).execute()
        disks = response.get('items', [])
        return disks

    def list_disk_types(self, **query):
        response = self.client.diskTypes().list(project=self.project_id, zone=self.zone).execute()
        disks_types = response.get('items', [])
        return disks_types

    def list_auto_scaler(self, **query):
        response = self.client.autoscalers().list(project=self.project_id, zone=self.zone).execute()
        auto_scaler = response.get('items', [])
        return auto_scaler

    def list_firewall(self, **query):
        response = self.client.firewalls().list(project=self.project_id).execute()
        firewall = response.get('items', [])
        return firewall

    def list_images(self, **query):
        response = self.client.images().list(project=self.project_id).execute()
        firewall = response.get('items', [])
        return firewall

    def list_instance_group(self, **query):
        response = self.client.instanceGroups().list(project=self.project_id).execute()
        firewall = response.get('items', [])
        return firewall

    def list_instance_group_manager(self, **query):
        response = self.client.instanceGroupManagers().list(project=self.project_id, zone=self.zone).execute()
        firewall = response.get('items', [])
        return firewall

    def _get_filter_to_params(self, **query):
        filtering_list = []
        filters = query.get('filter', None)
        if isinstance(filters, list) and filters is not None:
            for single_filter in filters:
                filter_key = single_filter.get('key', '')
                filter_values = single_filter.get('values', [])
                filter_str = self._get_full_filter_string(filter_key, filter_values)
                if filter_str != '':
                    filtering_list.append(filter_str)

            return ' AND '.join(filtering_list)

    def generate_query(self, is_default=False, **query):
        if is_default:
            query.update({
                'project': self.project_id,
                'zone': self.zone
            })
        return query

    def generate_key_query(self, key, value, delete, is_default=False, **query):
        if is_default:
            if delete != '':
                query.pop(delete, None)

            query.update({
                key: value,
                'project': self.project_id,
                'zone': self.zone
            })

        return query

    @staticmethod
    def get_region(zone):
        index = zone.find('-')
        region = zone[0:index] if index > -1 else ''
        return region

    @staticmethod
    def _get_full_filter_string(filter_key, filter_values):
        filter_string = ''
        if filter_key != '' and filter_values != [] and isinstance(filter_values, list):
            single_filter_list = [f'{filter_key}={x}' for x in filter_values]
            join_string = ' OR '.join(single_filter_list)
            filter_string = f'({join_string})'
        elif filter_key != '' and filter_values != [] and not isinstance(filter_values, dict):
            filter_string = f'({filter_key}={filter_values})'
        return filter_string
