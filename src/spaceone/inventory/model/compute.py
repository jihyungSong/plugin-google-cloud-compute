from schematics import Model
from schematics.types import  StringType, DateTimeType, DictType


class Compute(Model):
    keypair = StringType()
    az = StringType() # zone_name
    region_name = StringType()  # Zone name?
    instance_id = StringType()
    instance_name = StringType(default='')
    instance_state = StringType(choices=('STAGING', 'RUNNING', 'STOPPING', 'REPAIRING'))
    instance_type = StringType()
    account = StringType()
    image = StringType()
    launched_at = DateTimeType()
    tags = DictType(StringType, default={})
