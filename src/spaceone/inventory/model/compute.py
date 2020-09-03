from schematics import Model
from schematics.types import ListType, StringType, DateTimeType, DictType


class Compute(Model):
    keypair = StringType(default="")
    public_ip_address = StringType()
    az = StringType()
    instance_id = StringType()
    instance_name = StringType(default='')
    instance_state = StringType(choices=('PROVISIONING', 'STAGING', 'RUNNING', 'STOPPING', 'REPAIRING', 'SUSPENDING', 'SUSPENDED', 'TERMINATED'))
    instance_type = StringType()
    account_id = StringType()
    image = StringType()
    launched_at = DateTimeType()
    sg_group_names = ListType(StringType, default=[])
    tags = DictType(StringType, default={})
