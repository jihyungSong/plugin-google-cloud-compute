from schematics import Model
from schematics.types import StringType


class VPC(Model):
    vpc_id = StringType()
    vpc_name = StringType(default="")
    description = StringType(default="")
    self_link = StringType(default="")
