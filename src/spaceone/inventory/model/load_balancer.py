from schematics import Model
from schematics.types import StringType, IntType, DictType, ListType


class LoadBalancer(Model):
    type = StringType(choices=('HTTP', 'TCP', 'UDP'))
    name = StringType()
    dns = StringType(default="")
    port = ListType(IntType())
    protocol = ListType(StringType())
    scheme = StringType(choices=('EXTERNAL', 'INTERNAL'))
    tags = DictType(StringType, default={})

