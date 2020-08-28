from schematics import Model
from schematics.types import StringType, ModelType
from spaceone.inventory.model.vpc import VPC


class Subnet(Model):
    subnet_id = StringType()
    cidr = StringType()
    subnet_name = StringType()
    gateway_address = StringType()
    vpc = ModelType(VPC)
    self_link = StringType()
