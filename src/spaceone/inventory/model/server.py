from schematics import Model
from schematics.types import serializable, ModelType, ListType, StringType
from spaceone.inventory.model import OS, AWS, Hardware, SecurityGroupRule, Compute, LoadBalancer, VPC, Subnet, \
    AutoScalingGroup, NIC, Disk, ServerMetadata, Region


class ReferenceModel(Model):
    class Option:
        serialize_when_none = False

    resource_id = StringType(required=False, serialize_when_none=False)
    external_link = StringType(required=False, serialize_when_none=False)


class ServerData(Model):
    os = ModelType(OS)
    #os.domain
    gcp = ModelType(AWS)
    hardware = ModelType(Hardware)
    compute = ModelType(Compute)
    load_balancers = ListType(ModelType(LoadBalancer))
    security_group_rules = ListType(ModelType(SecurityGroupRule))
    #public_ip_address = StringType()
    #public_dns = StringType()
    vpc = ModelType(VPC)
    subnet = ModelType(Subnet)
    auto_scaling_group = ModelType(AutoScalingGroup, serialize_when_none=False)


class Server(Model):
    name = StringType()
    #server_id for later use.
    server_type = StringType(default='VM')
    os_type = StringType(choices=('LINUX', 'WINDOWS'))
    provider = StringType(default='gcp')
    primary_ip_address = StringType()
    ip_addresses = ListType(StringType())
    region_code = StringType(default='gcp')
    region_type = StringType(default='GCP')
    nics = ListType(ModelType(NIC))
    disks = ListType(ModelType(Disk))
    data = ModelType(ServerData)
    _metadata = ModelType(ServerMetadata, serialized_name='metadata')
    # reference = ModelType(ReferenceModel)

    @serializable
    def reference(self):
        return {
            "resource_id": f"arn:aws:gcp_compute:{self.data.compute.region_name}:{self.data.compute.account_id}:instance/{self.data.compute.instance_id}",
            "external_link": f"https://{self.data.compute.region_name}.console.aws.amazon.com/gcp_compute/v2/home?region={self.data.compute.region_name}#Instances:instanceId={self.data.compute.instance_id}"
        }

