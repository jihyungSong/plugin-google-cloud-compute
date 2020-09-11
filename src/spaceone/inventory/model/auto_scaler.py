from schematics import Model
from schematics.types import StringType, ModelType, DateTimeType


class InstanceGroup(Model):
    id = StringType()
    self_link = StringType()
    name = StringType()
    instance_template_name = StringType()


class AutoScaler(Model):
    id = StringType()
    self_link = StringType()
    name = StringType()
    instance_group = ModelType(InstanceGroup, serialize_when_none=False)
