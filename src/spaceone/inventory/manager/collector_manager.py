__all__ = ['CollectorManager']

import time
import logging
from pprint import pprint
from spaceone.core.manager import BaseManager
from spaceone.inventory.connector import GoogleCloudComputeConnector
from spaceone.inventory.manager.compute_engine import VMInstanceManager, AutoScalerManager, LoadBalancerManager, \
    DiskManager, NICManager, VPCManager, SecurityGroupRuleManager
from spaceone.inventory.manager.metadata.metadata_manager import MetadataManager
from spaceone.inventory.model.server import Server
from spaceone.inventory.model.region import Region


_LOGGER = logging.getLogger(__name__)


class CollectorManager(BaseManager):

    def __init__(self, transaction):
        super().__init__(transaction)

    def verify(self, options, secret_data):
        """ Check connection
        """
        gcp_connector = self.locator.get_connector('GoogleCloudComputeConnector')
        r = gcp_connector.verify(options, secret_data)
        # ACTIVE/UNKNOWN
        return r

    def list_regions(self, secret_data, region_name):
        gcp_connector: GoogleCloudComputeConnector = self.locator.get_connector('GoogleCloudComputeConnector')
        gcp_connector.set_client(secret_data, region_name)
        return gcp_connector.list_zones(secret_data)

    def list_instances(self, params):
        server_vos = []
        gcp_connector: GoogleCloudComputeConnector = self.locator.get_connector('GoogleCloudComputeConnector')
        gcp_connector.set_client(params['secret_data'], params['region_name'])

        # TODO:
        current_vo = self._get_simplified_vo(gcp_connector)

        instance_filter = {}

        if len(params.get('instance_ids', [])) > 0:
            instance_filter.update({'filter': [{'key': 'id', 'values': params['instance_ids']}]})

        instances = gcp_connector.list_instances(**instance_filter)

        print(f'===== [{params["region_name"]}]  /  INSTANCE COUNT : {len(instances)}')

        if len(instances) > 0:
            # Get Instance Type for GCP

            instance_group = gcp_connector.list_instance_group_managers()
            instance_types = gcp_connector.list_machine_types()

            # Image
            images = gcp_connector.list_images()

            # Autoscaling group list
            auto_scaler = gcp_connector.list_auto_scalers()

            # LB list
            load_balancers = gcp_connector.list_url_maps()

            # VPC
            vpcs = gcp_connector.list_vpcs()
            subnets = gcp_connector.list_subnets()

            # disks
            disks = gcp_connector.list_disk()
            disk_types = gcp_connector.list_disk_types()

            # Security Group(firewall)
            security_groups = gcp_connector.list_firewalls()

            # call_up all the managers
            vm_instance_manager: VMInstanceManager = VMInstanceManager(params)
            auto_scaler_manager: AutoScalerManager = AutoScalerManager(params, vm_connector=gcp_connector)
            elb_manager: LoadBalancerManager = LoadBalancerManager(params, vm_connector=gcp_connector)
            disk_manager: DiskManager = DiskManager(params)
            nic_manager: NICManager = NICManager(params)
            vpc_manager: VPCManager = VPCManager(params)
            security_group_manager: SecurityGroupRuleManager = SecurityGroupRuleManager(params)
            meta_manager: MetadataManager = MetadataManager()

            for instance in instances:
                server_data = vm_instance_manager.get_server_info(instance, instance_types, disks, current_vo)
                auto_scaler_vo = auto_scaler_manager.get_auto_scaler_info(instance, instance_group, auto_scaler)

                load_balancer_vos = elb_manager.get_load_balancer_info(load_balancers, target_groups,
                                                                       instance_id, instance_ip)

                disk_vos = disk_manager.get_disk_info(instance, disks)
                vpc_vo, subnet_vo = vpc_manager.get_vpc_info(instance, vpcs, subnets)

                nic_vos = nic_manager.get_nic_info(instance.get('NetworkInterfaces'), subnet_vo)

                sg_ids = [security_group.get('GroupId') for security_group in instance.get('SecurityGroups', []) if
                          security_group.get('GroupId') is not None]
                sg_rules_vos = sg_manager.get_security_group_rules_info(sg_ids, sgs)

                server_data.update({
                    'nics': nic_vos,
                    'disks': disk_vos,
                })

                server_data['data'].update({
                    'load_balancers': load_balancer_vos,
                    'security_group_rules': sg_rules_vos,
                    'auto_scaling_group': auto_scaler_vo,
                    'vpc': vpc_vo,
                    'subnet': subnet_vo,
                })

                # IP addr : ip_addresses = data.compute.eip + nics.ip_addresses + data.public_ip_address
                server_data.update({
                    'ip_addresses': self.merge_ip_addresses(server_data)
                })

                server_data['data']['compute']['account'] = project_id

                server_data.update({
                    '_metadata': meta_manager.get_metadata(),
                })

                server_vos.append(Server(server_data, strict=False))

        return server_vos

    def list_resources(self, params):
        '''
        params = {
            'region_name': target_region,
            'query': query,
            'secret_data': 'secret_data',
            'instance_ids': [instance_id, instance_id, ...]
        }
        '''
        start_time = time.time()

        try:
            resources = self.list_instances(params)
            print(f'   [{params["region_name"]}] Finished {time.time() - start_time} Seconds')
            return resources

        except Exception as e:
            print(f'[ERROR: {params["region_name"]}] : {e}')
            return []

    def get_volume_ids(self, instance):
        block_device_mappings = instance.get('BlockDeviceMappings', [])
        return [block_device_mapping['Ebs']['VolumeId'] for block_device_mapping in block_device_mappings if block_device_mapping.get('Ebs') is not None]

    def get_image_ids(self, instances):
        return [instance.get('ImageId') for instance in instances if instance.get('ImageId') is not None]

    def merge_ip_addresses(self, server_data):
        compute_data = server_data['data']['compute']
        nics = server_data['nics']

        nic_ip_addresses = []
        for nic in nics:
            nic_ip_addresses.extend(nic.ip_addresses)

        merge_ip_address = compute_data.eip + nic_ip_addresses

        if server_data['data']['public_ip_address'] != '':
            merge_ip_address.append(server_data['data']['public_ip_address'])

        return list(set(merge_ip_address))

    @staticmethod
    def _get_simplified_vo(vm_connector):
        return {
            'project_id': vm_connector.get('project_id', ''),
            'region': vm_connector.get('region', ''),
            'zone': vm_connector.get('zone', '')
        }

    @staticmethod
    def get_region_from_result(result):
        REGION_INFO = {
            'us-east-1': {'name': 'US East (N. Virginia)', 'tags': {'latitude': '39.028760', 'longitude': '-77.458263'}},
            'us-east-2': {'name': 'US East (Ohio)', 'tags': {'latitude': '40.103564', 'longitude': '-83.200092'}},
            'us-west-1': {'name': 'US West (N. California)', 'tags': {'latitude': '37.242183', 'longitude': '-121.783380'}},
            'us-west-2': {'name': 'US West (Oregon)', 'tags': {'latitude': '45.841046', 'longitude': '-119.658093'}},
            'af-south-1': {'name': 'Africa (Cape Town)', 'tags': {'latitude': '-33.932268', 'longitude': '18.424434'}},
            'ap-east-1': {'name': 'Asia Pacific (Hong Kong)', 'tags': {'latitude': '22.365560', 'longitude': '114.119420'}},
            'ap-south-1': {'name': 'Asia Pacific (Mumbai)', 'tags': {'latitude': '19.147428', 'longitude': '73.013805'}},
            'ap-northeast-3': {'name': 'Asia Pacific (Osaka-Local)', 'tags': {'latitude': '34.675638', 'longitude': '135.495706'}},
            'ap-northeast-2': {'name': 'Asia Pacific (Seoul)', 'tags': {'latitude': '37.528547', 'longitude': '126.871867'}},
            'ap-southeast-1': {'name': 'Asia Pacific (Singapore)', 'tags': {'latitude': '1.321259', 'longitude': '103.695942'}},
            'ap-southeast-2	': {'name': 'Asia Pacific (Sydney)', 'tags': {'latitude': '-33.921423', 'longitude': '151.188076'}},
            'ap-northeast-1': {'name': 'Asia Pacific (Tokyo)', 'tags': {'latitude': '35.648411', 'longitude': '139.792566'}},
            'ca-central-1': {'name': 'Canada (Central)', 'tags': {'latitude': '43.650803', 'longitude': '-79.361824'}},
            'cn-north-1': {'name': 'China (Beijing)', 'tags': {'latitude': '39.919635', 'longitude': '116.307237'}},
            'cn-northwest-1': {'name': 'China (Ningxia)', 'tags': {'latitude': '37.354511', 'longitude': '106.106147'}},
            'eu-central-1': {'name': 'Europe (Frankfurt)', 'tags': {'latitude': '50.098645', 'longitude': '8.632262'}},
            'eu-west-1': {'name': 'Europe (Ireland)', 'tags': {'latitude': '53.330893', 'longitude': '-6.362217'}},
            'eu-west-2': {'name': 'Europe (London)', 'tags': {'latitude': '51.519749', 'longitude': '-0.087804'}},
            'eu-south-1': {'name': 'Europe (Milan)', 'tags': {'latitude': '45.448648', 'longitude': '9.147316'}},
            'eu-west-3': {'name': 'Europe (Paris)', 'tags': {'latitude': '48.905302', 'longitude': '2.369778'}},
            'eu-north-1': {'name': 'Europe (Stockholm)', 'tags': {'latitude': '59.263542', 'longitude': '18.104861'}},
            'me-south-1': {'name': 'Middle East (Bahrain)', 'tags': {'latitude': '26.240945', 'longitude': '50.586321'}},
            'sa-east-1': {'name': 'South America (São Paulo)', 'tags': {'latitude': '-23.493549', 'longitude': '-46.809319'}},
            'us-gov-east-1': {'name': 'AWS GovCloud (US-East)'},
            'us-gov-west-1': {'name': 'AWS GovCloud (US)'},
        }

        match_region_info = REGION_INFO.get(getattr(result.data.compute, 'region_name', None))

        if match_region_info is not None:
            region_info = match_region_info.copy()
            region_info.update({
                'region_code': result.data.compute.region_name
            })

            return Region(region_info, strict=False)

        return None
