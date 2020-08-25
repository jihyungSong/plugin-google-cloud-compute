__all__ = ['CollectorManager']

import time
import logging
import concurrent.futures
from spaceone.core.manager import BaseManager
from spaceone.inventory.connector import GoogleCloudComputeConnector
from spaceone.inventory.manager.compute_engine import VMInstanceManager, AutoScalerManager, LoadBalancerManager, \
    DiskManager, NICManager, VPCManager, SecurityGroupRuleManager
from spaceone.inventory.manager.metadata.metadata_manager import MetadataManager
from spaceone.inventory.model.server import Server
from spaceone.inventory.model.region import Region


_LOGGER = logging.getLogger(__name__)
NUMBER_OF_CONCURRENT = 20


class CollectorManager(BaseManager):

    gcp_connector = None

    def __init__(self, transaction):
        super().__init__(transaction)

    def verify(self, options, secret_data):
        """ Check connection
        """
        self.gcp_connector = self.locator.get_connector('GoogleCloudComputeConnector')
        r = self.gcp_connector.verify(options, secret_data)
        # ACTIVE/UNKNOWN
        return r

    def set_connector(self, secret_data):
        self.gcp_connector: GoogleCloudComputeConnector = self.locator.get_connector('GoogleCloudComputeConnector')
        self.gcp_connector.get_connect(secret_data)

    def list_regions(self, secret_data):
        if self.gcp_connector is None:
            self.set_connector(secret_data)

        return self.gcp_connector.list_regions()

    def list_zones(self, secret_data):
        if self.gcp_connector is None:
            self.set_connector(secret_data)

        return self.gcp_connector.list_zones()

    def list_instances(self, params):
        connector = params['connector']

        server_vos = []
        instance_filter = {'zone': params['zone_info']['zone']}

        if len(params.get('instance_ids', [])) > 0:
            instance_filter.update({'filter': [{'key': 'id', 'values': params['instance_ids']}]})

        instances = connector.list_instances(**instance_filter)

        if len(instances) > 0:
            resources = params['resources']

            # Images
            images = resources.get('images', [])

            # VPC
            vpcs = resources.get('vpcs', [])
            subnets = resources.get('subnets', [])

            # URL Maps
            load_balancers = resources.get('url_maps', [])

            # Forwarding Rules
            forwarding_rules = resources.get('forwarding_rules', [])

            # Security Group (Firewall)
            security_groups = resources.get('firewalls', [])

            # Get Instance Groups
            instance_group = connector.list_instance_group_managers()

            # Get Machine Types
            instance_types = connector.list_machine_types()

            # Autoscaling group list
            auto_scaler = connector.list_auto_scalers()

            # disks
            disks = connector.list_disk()
            disk_types = connector.list_disk_types()

            # call_up all the managers
            vm_instance_manager: VMInstanceManager = VMInstanceManager(params)
            auto_scaler_manager: AutoScalerManager = AutoScalerManager(params)
            lb_manager: LoadBalancerManager = LoadBalancerManager(params)
            disk_manager: DiskManager = DiskManager(params)
            nic_manager: NICManager = NICManager(params)
            vpc_manager: VPCManager = VPCManager(params)
            security_group_manager: SecurityGroupRuleManager = SecurityGroupRuleManager(params)
            meta_manager: MetadataManager = MetadataManager()

            # for instance in instances:
            #     server_data = vm_instance_manager.get_server_info(instance, instance_types, disks)
            #     auto_scaler_vo = auto_scaler_manager.get_auto_scaler_info(instance, instance_group, auto_scaler)
            #
            #     # load_balancer_vos = elb_manager.get_load_balancing_info(load_balancers, target_groups,
            #     #                                                        instance_id, instance_ip)
            #
            #     disk_vos = disk_manager.get_disk_info(instance, disks)
            #     vpc_vo, subnet_vo = vpc_manager.get_vpc_info(instance, vpcs, subnets)
            #     nic_vos = nic_manager.get_nic_info(instance, subnet_vo)
            #
            #     # sg_ids = [security_group.get('GroupId') for security_group in instance.get('SecurityGroups', []) if
            #     #           security_group.get('GroupId') is not None]
            #     # sg_rules_vos = sg_manager.get_security_group_rules_info(sg_ids, sgs)
            #
            #     server_data.update({
            #         'nics': nic_vos,
            #         'disks': disk_vos,
            #     })
            #
            #     server_data['data'].update({
            #         'load_balancers': load_balancer_vos,
            #         'security_group_rules': sg_rules_vos,
            #         'auto_scaler_group': auto_scaler_vo,
            #         'vpc': vpc_vo,
            #         'subnet': subnet_vo,
            #     })
            #
            #     # IP addr : ip_addresses = data.compute.eip + nics.ip_addresses + data.public_ip_address
            #     server_data.update({
            #         'ip_addresses': self.merge_ip_addresses(server_data)
            #     })
            #
            #     server_data['data']['compute']['account'] = project_id
            #
            #     server_data.update({
            #         '_metadata': meta_manager.get_metadata(),
            #     })
            #
            #     server_vos.append(Server(server_data, strict=False))

        return server_vos

    def list_resources(self, params):
        '''
        params = {
            'connector': GoogleCloudComputeConnector,
            'zone_info': {
               'region': 'us-east-1,
               'zone': 'us-east-1a'
            },
            'query': query,
            'secret_data': 'secret_data',
            'instance_ids': [instance_id, instance_id, ...],
            'resources': {
                'url_maps': url_maps,
                'images': images,
                'vpcs': vpcs,
                'fire_walls': fire_walls,
                'subnets': subnets,
                'forwarding_rules': forwarding_rules
            }
        }
        '''

        print(f"START LIST Resources {params['zone_info']['zone']}")
        start_time = time.time()

        try:
            resources = self.list_instances(params)
            print(f'   [{params["zone_info"]["zone"]}] Finished {time.time() - start_time} Seconds')
            return resources

        except Exception as e:
            print(f'[ERROR: {params["zone_info"]["zone"]}] : {e}')
            return []

    def list_subnets(self, params):
        '''
        params = {
            'region': 'GOOGLE_REGION',
            'connector': GoogleCloudComputeConnector
        }
        '''
        print(f"[START] LIST Subnet {params['region']}")
        connector: GoogleCloudComputeConnector = params['connector']
        subnets = connector.list_subnets(region=params['region'])
        print(f"[END] {params['region']}")
        # return self.gcp_connector.list_subnets(region=params['region'])
        return subnets

    def list_forwarding_rules(self, params):

        '''
        params = {
            'region': 'GOOGLE_REGION',
            'connector': GoogleCloudComputeConnector
        }
        '''
        print(f"LIST Forwarding Rules START.. {params['region']}")
        connector: GoogleCloudComputeConnector = params['connector']
        frules = connector.list_forwarding_rules(region=params['region'])
        print(f"[END] {params['region']}")
        # return self.gcp_connector.list_forwarding_rules(region=params['region'])
        return frules

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

    def get_zone_independent_resources(self, secret_data, regions):
        print("[ GET zone independent resources ]")
        if self.gcp_connector is None:
            self.set_connector(secret_data)

        url_maps = self.gcp_connector.list_url_maps()
        images = self.gcp_connector.list_images()
        vpcs = self.gcp_connector.list_vpcs()
        fire_walls = self.gcp_connector.list_firewalls()
        subnets = []
        forwarding_rules = []

        mt_params = self.generate_mt_params(secret_data, regions)

        # Generate Thread Pool for collecting Subnets
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_CONCURRENT) as executor:
            future_executors = []
            for mt_param in mt_params:
                future_executors.append(executor.submit(self.list_subnets, mt_param))

            for future in concurrent.futures.as_completed(future_executors):
                for result in future.result():
                    subnets.append(result)

        # Generate Thread Pool for collecting Forwarding Rules
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_CONCURRENT) as executor:
            future_executors = []
            for mt_param in mt_params:
                future_executors.append(executor.submit(self.list_forwarding_rules, mt_param))

            for future in concurrent.futures.as_completed(future_executors):
                for result in future.result():
                    forwarding_rules.append(result)

        print("====== END of zone independent resources")

        return {
            'url_maps': url_maps,
            'images': images,
            'vpcs': vpcs,
            'fire_walls': fire_walls,
            'subnets': subnets,
            'forwarding_rules': forwarding_rules
        }

    def generate_mt_params(self, secret_data, regions):
        params = []

        for region in regions:
            _conn = self.locator.get_connector('GoogleCloudComputeConnector')
            _conn.get_connect(secret_data)

            params.append({
                'region': region['name'],
                'connector': _conn
            })

        return params
        #return list(map(lambda region: {'region': region['name']}, regions))

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
            'asia-east1': {'name': 'Changhua County, Taiwan'},
            'asia-east2': {'name': 'Hong Kong'},
            'asia-northeast1': {'name': 'Tokyo, Japan'},
            'asia-northeast2': {'name': 'Osaka, Japan'},
            'asia-northeast3': {'name': 'Seoul, South Korea'},
            'asia-south1': {'name': 'Mumbai, India'},
            'asia-southeast1': {'name': 'Jurong West, Singapore'},
            'asia-southeast2': {'name': 'Jakarta, Indonesia'},
            'australia-southeast1': {'name': 'Sydney, Australia'},
            'europe-north1': {'name': 'Hamina, Finland'},
            'europe-west1': {'name': 'St. Ghislain, Belgium'},
            'europe-west2': {'name': 'London, England, UK'},
            'europe-west3': {'name': 'Frankfurt, Germany'},
            'europe-west4': {'name': 'Eemshaven, Netherlands'},
            'europe-west6': {'name': 'Zürich, Switzerland'},
            'northamerica-northeast1': {'name': 'Montréal, Québec, Canada'},
            'southamerica-east1': {'name': 'Osasco (São Paulo), Brazil'},
            'us-central1': {'name': 'Council Bluffs, Iowa, USA'},
            'us-east1': {'name': 'Moncks Corner, South Carolina, USA'},
            'us-east4': {'name': 'Ashburn, Northern Virginia, USA'},
            'us-west1': {'name': 'The Dalles, Oregon, USA'},
            'us-west2': {'name': 'Los Angeles, California, USA'},
            'us-west3': {'name': 'Salt Lake City, Utah, USA'},
            'us-west4': {'name': 'Las Vegas, Nevada, USA'},
        }

        match_region_info = REGION_INFO.get(result.region_code)

        if match_region_info is not None:
            region_info = match_region_info.copy()
            region_info.update({
                'region_code': result.region_code
            })

            return Region(region_info, strict=False)

        return None

