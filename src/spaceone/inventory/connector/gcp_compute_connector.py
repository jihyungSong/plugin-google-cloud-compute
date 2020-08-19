__all__ = ["GcpComputeConnector"]

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


class GcpComputeConnector(BaseConnector):

    def __init__(self, transaction=None, conf=None):
        self.client = None
        self.project_id = None
        self.zone = None

    def verify(self, options, secret_data):
        self.get_connect(secret_data)
        return "ACTIVE"

    def get_connect(self, secret_data, service="gcp_compute"):
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

    def set_client(self, secret_data, region_name):
        self.client = self.get_connect(secret_data)
        self.project_id = secret_data.get('project_id')
        self.zone = region_name

    def list_regions(self, secret_data):
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
        query = self.generate_query(is_paginate=True, **query)
        result = self.client.machineTypes().list(**query).execute()
        instance_types = result.get('items', [])
        return instance_types

    def collectInfo(self, query, region_id=None, zone_id=None, pool_id=None, project_id=None):
        (query, instance_ids) = self._checkQuery(query)

        '''
        https://cloud.google.com/compute/docs/reference/rest/v1/instances/list?hl=ko
        '''

        return self._listInstances(region_id, zone_id, pool_id, project_id, query, instance_ids)

    def _listInstances(self, region_id, zone_id, pool_id, project_id, query, instance_ids):

        instance_query = {}  # TODO: filter

        # make region filter
        zone_list = self._call_zone_list()

        for zone in zone_list:
            instances = self._call_instance_list(zone)

            for instance in instances:
                # get machine type dict

                server_data_dic = {}
                # data.default
                ret = self._composite_default_data(instance, pool_id, project_id, region_id, zone_id)
                server_data_dic.update(ret)

                mtype_dic = self._parse_machine_type(self.project_id, zone, instance)

                # resource.data.base
                ret = self._composite_base_data(mtype_dic)
                server_data_dic["resource"] = deep_merge(ret, server_data_dic["resource"])

                # resource.data.os
                ret = self._composite_os_data()
                server_data_dic["resource"] = deep_merge(ret, server_data_dic["resource"])

                # resources.data.compute
                ret = self._composit_compute_data(instance, mtype_dic)

                server_data_dic["resource"] = deep_merge(ret, server_data_dic["resource"])

                # data.platform

                ret = self._composite_platform_data(instance)
                server_data_dic["resource"] = deep_merge(ret, server_data_dic["resource"])

                # data.nics
                ret = self._composite_nics_data(instance, zone)
                server_data_dic["resource"] = deep_merge(ret, server_data_dic["resource"])

                # data.disk
                ret = self._composite_disk_data(instance, zone)
                server_data_dic["resource"] = deep_merge(ret, server_data_dic["resource"])

                # data.compute.firewalls
                ret = self._composite_firewall_data(instance)
                server_data_dic["resource"] = deep_merge(ret, server_data_dic["resource"])

                ret = self._create_metadata()

                server_data_dic["resource"] = deep_merge(ret, server_data_dic["resource"])

                # resource.meta

                server_data_dic = ddict2dict(server_data_dic)

                yield server_data_dic

        # return resource_list

    def _composite_default_data(self, instance, pool_id, project_id, region_id, zone_id):
        ret_default_dic = nested_dict()
        ret_default_dic['state'] = 'SUCCESS'
        ret_default_dic['resource_type'] = DATA_INFO['VM']['resource_type']
        ret_default_dic['match_rules'] = DATA_INFO['VM']['MATCH_RULES']

        ret_default_dic['resource'] = {}
        ret_default_dic["resource"]['name'] = instance['name']
        ret_default_dic['resource']['data'] = {}
        ret_default_dic['resource']['server_type'] = 'VM'

        if region_id != None:
            ret_default_dic["resource"]['region_id'] = region_id
        if zone_id != None:
            ret_default_dic["resource"]['zone_id'] = zone_id
        if pool_id != None:
            ret_default_dic["resource"]['pool_id'] = pool_id
        if project_id != None:
            ret_default_dic["resource"]['project_id'] = project_id

        return ret_default_dic

    def _composite_disk_data(self, instance, zone):
        ret_dic = nested_dict()
        ret_dic['disks'] = []
        disk_device_index = 0
        for disk in instance['disks']:
            disk_dic = {}

            # get disktype : size ,volume id
            disktype_name = disk.get('source', 'Unknown')
            disktype_dic = self._parse_disk_type(self.project_id, zone, disktype_name)

            disk_tags_type_item = (disktype_dic.get("type", "Unknown")).split("/")
            disk_dic["tags"] = {}
            disk_dic["tags"]["ebs_type"] = disk_tags_type_item[-1]
            disk_dic["tags"]['ebs_id'] = disktype_dic["id"]

            # get os distro
            getosdistros = disktype_dic.get("licenses", "Unknown")
            for getosdistro in getosdistros:
                getosdistroitem = getosdistro.split("/")
                ret_dic['data']['os']["os_version"] = getosdistroitem[-1]
                ret_dic['data']['os']["os_arch"] = ""
                if "windows" in ret_dic['data']['os']["os_version"]:
                    ret_dic["os_type"] = "WINDOWS"
                else:
                    ret_dic["os_type"] = "LINUX"

            # get image name
            if "sourceImage" in disktype_dic.keys():
                sourceimagetype_name = disktype_dic.get("sourceImage", 'Unknown')
                sourceimagetype_dic = self._parse_sourceImage_type(sourceimagetype_name)
                # insert imagetype
                ret_dic['data']["compute"]["image"] = sourceimagetype_dic['name']
                ret_dic['data']["os"]["os_details"] = sourceimagetype_dic[
                    "description"] if "description" in sourceimagetype_dic else ""

            disk_dic['disk_type'] = disk['type']
            disk_dic['device'] = disk['deviceName']
            disk_dic['device_index'] = disk['index']

            disk_dic['size'] = disktype_dic["sizeGb"]

            ret_dic['disks'].append(disk_dic)
        # print(json.loads(json.dumps(ret_dic)))

        return ret_dic

    def _composite_nics_data(self, instance, zone):

        ret_dic = nested_dict()
        ret_dic['ip_addresses'] = []
        ret_dic['nics'] = []
        ret_dic['ip_addresses'] = []
        nic_device_index = 0

        for nic in instance['networkInterfaces']:

            nic_dics = {}
            nic_dics['ip_addresses'] = []

            nic_dics['device_index'] = nic_device_index
            # nic_dic['mac_address'] = nic['MacAddress']
            if 'accessConfigs' in nic:
                for accessConfig in nic['accessConfigs']:
                    ret_dic['data']['compute']['static_nat'] = []
                    ret_dic['data']['compute']['static_nat'].append(accessConfig.get('natIp'))

            nic_ip = {}
            nic_ip['ip_address'] = nic['networkIP']

            subnetwork_name = nic.get('subnetwork', 'Unknown')

            subnetwork_dic = self._parse_subnetwork_type(self.project_id, zone, subnetwork_name)

            nic_ip['cidr'] = subnetwork_dic['ipCidrRange']

            nic_dics['ip_addresses'].append(nic_ip)

            ret_dic['nics'].append(nic_dics)
            ret_dic['ip_addresses'].append(nic['networkIP'])
            nic_device_index = nic_device_index + 1

        return ret_dic

    def _composite_platform_data(self, instance):

        ret_dic = nested_dict()

        ret_dic['data']['platform']['type'] = 'GCP'

        return ret_dic

    def _composite_base_data(self, mtype_dic):

        ret_dic = nested_dict()
        ret_dic['data']['base']['core'] = mtype_dic['guestCpus']
        ret_dic['data']['base']['memory'] = round(mtype_dic['memoryMb'] / 1024, 2)

        return ret_dic

    def _composite_os_data(self):
        ret_dic = nested_dict()

        return ret_dic

    def _composit_compute_data(self, instance, mtype_dic):
        ret_dic = nested_dict()
        ret_dic['data']['compute']['instance_id'] = instance['id']
        ret_dic['data']['compute']['instance_name'] = instance['name']

        ret_dic['data']['compute']['instance_type'] = mtype_dic['name']
        ret_dic['data']['compute']['static_nat'] = []

        if "items" in instance["metadata"].keys():
            keypairs = []
            # todo

            for item in instance["metadata"]["items"]:
                if item["key"] == "ssh-keys":
                    key_list = item["value"].split("\n")
                    for key in key_list:
                        key_name = key.split(":")
                        keypairs.append(key_name[0])

            ret_dic["data"]["compute"]["metadata_items"] = instance["metadata"]["items"]
            ret_dic["data"]["compute"]["keypairs"] = keypairs

        # print(mtype_dic)

        return ret_dic

    def _composite_firewall_data(self, instance):
        ret_security_group_rules_list = []
        ret_security_group_rules_name = []
        ret_dic = nested_dict()
        firewalls = []
        vpcs = []
        tags = []
        svcs = []

        firewalls = self._get_firewall_list(self.project_id)
        vpcs = self._get_vpc_list(instance)
        tags = self._get_tag_list(instance)
        svcs = self._get_svc(instance)

        for firewall in firewalls:
            # print(firewall)
            items = firewall["network"].split("/")
            firewall_vpc = items[-1]
            # print(firewall)

            if firewall_vpc in vpcs:

                if "targetTags" in firewall.keys():
                    firewall_target_tags_list = firewall["targetTags"]

                    for firewall_target_tag in firewall_target_tags_list:

                        if firewall_target_tag in tags:
                            ret_security_group_rules_list.extend(self.make_firewall_dict("targetTags", firewall))
                            ret_security_group_rules_name.append(firewall["name"])

                elif "targetServiceAccounts" in firewall.keys():

                    firewall_target_serviceaccount_list = firewall["targetServiceAccounts"]
                    for firewall_target_serviceaccount in firewall_target_serviceaccount_list:

                        if firewall_target_serviceaccount == svcs:
                            ret_security_group_rules_list.extend(
                                self.make_firewall_dict("targetServiceAccounts", firewall))
                            ret_security_group_rules_name.append(firewall["name"])

                elif "targetTags" not in firewall.keys() and "targetServiceAccounts" not in firewall.keys():
                    ret_security_group_rules_list.extend(self.make_firewall_dict("all", firewall))
                    ret_security_group_rules_name.append(firewall["name"])

        ret_dic["data"]["security_group_rules"] = ret_security_group_rules_list
        ret_dic["data"]["compute"]["security_groups"] = ret_security_group_rules_name
        return ret_dic
        # firewall_tags = firewall["targetTags"]

    def make_firewall_dict(self, firewall_flag=str, firewall=dict):
        firewall_dict_list = []
        sg_dict = {}

        security_group_id = []
        security_group_name = []
        direction = []
        priority = []
        action = []

        src_name_cidr = []

        src_port_range_min = []
        src_port_range_max = []

        protocol = []

        dst_name_cidr = []
        dst_port_range_min = []
        dst_port_range_max = []

        security_group_id.append(firewall["id"])
        security_group_name.append(firewall["name"])

        priority.append(firewall["priority"])
        action.append("allow") if "allowed" in firewall.keys() else firewall_action.append("deny")

        if "INGRESS" in firewall["direction"]:
            direction.append("inbound")
            if "sourceTags" in firewall.keys():
                src_name_cidr.extend(firewall["sourceTags"])

            if "sourceServiceAccounts" in firewall.keys():
                src_name_cidr.extend(firewall["sourceServiceAccounts"])

            if "sourceRanges" in firewall.keys():
                src_name_cidr.extend(firewall["sourceRanges"])

            if (firewall_flag == "targetTags"):
                dst_name_cidr.extend(firewall[firewall_flag])
            elif (firewall_flag == "targetServiceAccounts"):
                dst_name_cidr.extend(firewall[firewall_flag])
            else:
                dst_name_cidr.append("VPC: all")

            # dst_name_cidr.append("SELF")


        else:
            direction.append("outbound")

            if "destinationRanges" in firewall.keys():
                dst_name_cidr.extend(firewall["destinationRanges"])

            if (firewall_flag == "targetTags"):
                src_name_cidr.extend(firewall[firewall_flag])

            elif (firewall_flag == "targetServiceAccounts"):
                src_name_cidr.extend(firewall[firewall_flag])
            else:
                src_name_cidr.append("VPC: all")

            # src_name_cidr.append("SELF")

        # ALLOW or Deny 루프 한번 돌아야 하니 나중에

        sg_dict["security_group_id"] = security_group_id
        sg_dict["security_group_name"] = security_group_name
        sg_dict["direction"] = direction
        sg_dict["action"] = action
        sg_dict["priority"] = priority

        sg_dict["src"] = src_name_cidr
        # sg_dict["src_cidr"] = src_cidr
        sg_dict["dst"] = dst_name_cidr
        # sg_dict["dst_cidr"] = dst_cidr
        # if "allowed" in firewall.keys():

        # print(firewall_dict)
        # print(firewall)
        if "allowed" in firewall.keys():
            firewall_dict_list.extend(self.make_firewall_seperated_list("allowed", firewall, sg_dict))

        else:
            firewall_dict_list.extend(self.make_firewall_seperated_list('denied', firewall, sg_dict))

        return firewall_dict_list

    def make_firewall_seperated_list(self, state, firewall, sg_dict):
        ret_list = []
        # print(sg_dict)
        for sg_ipprotocol_dict in firewall[state]:
            sg_ipprotocol_dict['IPProtocol'] = sg_ipprotocol_dict['IPProtocol'].split(" ")
            sg_dict["protocol"] = sg_ipprotocol_dict['IPProtocol']
            if "ports" in sg_ipprotocol_dict.keys():
                sg_dict["port_range"] = sg_ipprotocol_dict["ports"]
            # print(sg_dict)
            sg_dict_list = (dict(zip(sg_dict, x)) for x in itertools.product(*sg_dict.values()))

            for dic in sg_dict_list:

                p = re.compile("^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?$")

                match_src = p.match(dic["src"])
                match_dst = p.match(dic["dst"])

                if match_src:
                    dic["src_cidr"] = dic["src"]
                else:
                    dic["src_name"] = dic["src"]

                if match_dst:
                    dic["dst_cidr"] = dic["dst"]
                else:
                    dic["dst_name"] = dic["dst"]

                # print(dic)
                dic['tags'] = {}
                if "port_range" in dic.keys():
                    port_range_list = dic["port_range"].split("-")

                    if state == "allowed":
                        dic["src_port_range_min"] = 0
                        dic["src_port_range_max"] = 65535

                        if len(port_range_list) == 2:
                            dic["dst_port_range_min"] = int(port_range_list[0])
                            dic["dst_port_range_max"] = int(port_range_list[1])

                            del dic["port_range"]
                        else:
                            dic["dst_port_range_min"] = int(port_range_list[0])
                            dic["dst_port_range_max"] = int(port_range_list[0])
                            del dic["port_range"]
                    else:
                        dic["dst_port_range_min"] = 0
                        dic["dst_port_range_max"] = 65535
                        if len(port_range_list) == 2:
                            dic["src_port_range_min"] = int(port_range_list[0])
                            dic["src_port_range_max"] = int(port_range_list[1])

                            del dic["port_range"]
                        else:
                            dic["src_port_range_min"] = int(port_range_list[0])
                            dic["src_port_range_max"] = int(port_range_list[0])
                            del dic["port_range"]
                # print(dic)
                # print(ret_list)
                ret_list.append(dic)

        return ret_list

    def _parse_machine_type(self, project, zone, instance):
        '''
        https://cloud.google.com/compute/docs/reference/rest/v1/machineTypes/get?hl=ko
        '''
        mtype = instance.get('machineType', 'Unknown')
        items = mtype.split('/')
        request = self.client.machineTypes().get(project=self.project_id, zone=zone, machineType=items[-1]).execute()
        # print(request)

        return request

    def _parse_disk_type(self, project, zone, disktype):
        '''
        https://cloud.google.com/compute/docs/reference/rest/v1/disks/get?hl=ko
        '''
        items = disktype.split("/")

        request = self.client.disks().get(project=self.project_id, zone=zone, disk=items[-1]).execute()

        return request

    def _parse_sourceImage_type(self, sourceimagetype):
        '''
        https://cloud.google.com/compute/docs/reference/rest/v1/images/get?hl=ko
        '''

        items = sourceimagetype.split("/")
        request = self.client.images().get(project=items[-4], image=items[-1]).execute()

        return request

    def _parse_subnetwork_type(self, project, zone, subnetwork):
        '''
        https://cloud.google.com/compute/docs/reference/rest/v1/subnetworks/get?hl=ko
        '''
        items = subnetwork.split("/")

        request = self.client.subnetworks().get(project=self.project_id, region=items[-3],
                                                subnetwork=items[-1]).execute()

        return request

    def _get_firewall_list(self, project):
        '''
        https://cloud.google.com/compute/docs/reference/rest/v1/firewalls/list?hl=ko
        '''
        result = self.client.firewalls().list(project=self.project_id).execute()

        return result['items'] if 'items' in result else []

    def _get_vpc_list(self, instance):

        nics = instance["networkInterfaces"]
        ret_list = []
        for nic in nics:
            items = nic["network"].split("/")
            ret_list.append(items[-1])
        return ret_list

    def _get_tag_list(self, instance):
        ret_list = []
        if 'items' in instance["tags"].keys():
            ret_list = instance["tags"]["items"]
        return ret_list

    def _get_svc(self, instance):

        svc = instance["serviceAccounts"][0]["email"]

        return svc

    def _create_metadata(self):
        """ Create metadata for frontend view
        """

        details = self._create_details()
        sub_data = self._create_sub_data()

        metadata = {
            "metadata": {
                'details': details,
                'sub_data': sub_data
            }
        }
        return metadata

    def _create_details(self):
        """ Create detail
        # Compute
        """

        compute = {
            'name': 'Compute',
            'data_source': [
                {'name': 'Instance ID', 'key': 'data.compute.instance_id'},
                {'name': 'Key Pairs', 'key': 'data.compute.keypairs',
                 'view_type': 'list',
                 'view_option': {
                     'item': {
                         'view_type': 'text',
                     },
                 },
                 },
                {'name': 'Instance Type', 'key': 'data.compute.instance_type'},
                {'name': 'Image', 'key': 'data.compute.image'},
                {'name': 'Created By', 'key': 'data.compute.created_by_user_id'},
                {'name': 'Security Group', 'key': 'data.compute.security_groups',
                 'view_type': 'list',
                 'view_option': {
                     'item': {
                         'view_type': 'text',
                     },
                 },
                 },
            ]
        }

        details = [compute]
        return details

    def _create_sub_data(self):
        """ Create Sub Data page
        """
        disk = {
            'name': 'Disk',
            'view_type': 'table',
            'key_path': 'disks',
            'data_source': [
                {'name': 'Index', 'key': 'device_index'},
                {'name': 'Name', 'key': 'device'},
                {'name': 'Type', 'key': 'disk_type'},
                {'name': 'Size(GB)', 'key': 'size'}
            ]
        }

        nic = {
            'name': 'NIC',
            'view_type': 'table',
            'key_path': 'nics',
            'data_source': [
                {'name': 'Index', 'key': 'device_index'},
                {'name': 'MAC', 'key': 'mac_address'},
                {'name': 'IP', 'key': 'tags.ip_list',
                 'view_type': 'list',
                 'view_option': {
                     'item': {
                         'view_type': 'text',
                     },
                 },

                 }
            ]
        }

        sg_rules = {
            'name': 'Security Groups',
            'view_type': 'table',
            'key_path': 'data.security_group_rules',
            'data_source': [
                {'name': 'Direction', 'key': 'direction'},
                {'name': 'Priority', 'key': 'priority'},
                {'name': 'Action', 'key': 'action'},
                {'name': 'Source', 'key': 'src'},
                {'name': 'Source Port Min', 'key': 'src_port_range_min'},
                {'name': 'Source Port Max', 'key': 'src_port_range_max'},
                {'name': 'Protocol', 'key': 'protocol'},
                {'name': 'Destination', 'key': 'dst'},
                {'name': 'Destination Port Min', 'key': 'dst_port_range_min'},
                {'name': 'Destination Port Max', 'key': 'dst_port_range_max'}

            ]
        }

        metadata_items = {
            "name": "Instance MetaData",
            "view_type": "table",
            "key_path": "data.compute.metadata_items",
            "data_source": [
                {"name": "Key", "key": "key"},
                {"name": "value", "key": "value"}
            ]

        }

        sub_data = [disk, nic, sg_rules, metadata_items]
        return sub_data

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
    def _get_full_filter_string(filter_key, filter_values):
        filter_string = ''
        if filter_key != '' and filter_values != [] and isinstance(filter_values, list):
            single_filter_list = [f'{filter_key}={x}' for x in filter_values]
            join_string = ' OR '.join(single_filter_list)
            filter_string = f'({join_string})'
        elif filter_key != '' and filter_values != [] and not isinstance(filter_values, dict):
            filter_string = f'({filter_key}={filter_values})'
        return filter_string
