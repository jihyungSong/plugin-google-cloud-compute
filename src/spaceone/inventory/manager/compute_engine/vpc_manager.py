from spaceone.core.manager import BaseManager
from spaceone.inventory.model.vpc import VPC
from spaceone.inventory.model.subnet import Subnet


class VPCManager(BaseManager):

    def __init__(self, params, ec2_connector=None):
        self.params = params
        self.ec2_connector = ec2_connector

    def get_vpc_info(self, instance, vpcs, subnets):
        '''
        vpc_data = {
            "vpc_id": "",
            "vpc_name": "",
            "description": "",
            "self_link": ""
        }

        subnet_data = {
            "subnet_id": "",
            "subnet_name": "",
            "self_link": "",
            "gateway_address": "",
            "vpc" : VPC
            "cidr": ""
        }
        '''

        vpc_data = {}
        subnet_data = {}
        matched_subnet = self.get_subnet(instance, subnets)
        matched_vpc = self.get_vpc(matched_subnet, vpcs)

        # if match_vpc is not None:
        #     vpc_data.update({
        #         'vpc_arn': self.generate_arn('vpc', match_vpc.get('OwnerId'), match_vpc.get('VpcId'), region_name),
        #         'vpc_id': match_vpc.get('VpcId'),
        #         'cidr': match_vpc.get('CidrBlock'),
        #         'vpc_name': self.generate_name(match_vpc),
        #     })
        #
        # if match_subnet is not None:
        #     subnet_data.update({
        #         'subnet_name': self.generate_name(match_subnet),
        #         'subnet_arn': match_subnet.get('SubnetArn'),
        #         'subnet_id': match_subnet.get('SubnetId'),
        #         'cidr':  match_subnet.get('CidrBlock'),
        #     })

        return VPC(vpc_data, strict=False), Subnet(subnet_data, strict=False)

    def get_vpc(self, matched_subnet, vpcs):

        for vpc in vpcs:
            pass
        return None

    def get_subnet(self, instance, subnets):
        subnet_data = None
        subnet_work_links =[]
        network_interfaces = instance.get('networkInterfaces', [])
        for network_interface in network_interfaces:
            subnet_work = network_interface.get('subnetwork', '')
            if subnet_work != '':
                subnet_work_links.append(subnet_work)

        for subnet in subnets:
            if subnet.get('selfLink', '') in subnet_work_links:
                subnet_data = subnet
                break

        return subnet_data

    def generate_arn(self, resource_type, owner_id, resource_id, region_name):
        return f'arn:aws:ec2:{region_name}:{owner_id}:{resource_type}/{resource_id}'

    @staticmethod
    def generate_name(resource):
        for resource_tag in resource.get('Tags', []):
            if resource_tag['Key'] == "Name":
                return resource_tag["Value"]

        return ''
