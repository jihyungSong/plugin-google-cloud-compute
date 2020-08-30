from schematics import Model
from schematics.types import ListType, StringType, DateTimeType, DictType


class Compute(Model):
    keypair = StringType(default="")
    az = StringType()                       # zone_name
    instance_id = StringType()
    instance_name = StringType(default='')
    instance_state = StringType(choices=('STAGING', 'RUNNING', 'STOPPING', 'REPAIRING'))
    instance_type = StringType()
    account = StringType()                  # Project_id
    image = StringType()
    launched_at = DateTimeType()
    sg_group_names = ListType(StringType, default=[])
    tags = DictType(StringType, default={})
