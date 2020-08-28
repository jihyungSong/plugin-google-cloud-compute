from schematics import Model
from schematics.types import IntType, FloatType, StringType, BooleanType


class Hardware(Model):
    core = IntType(default=0)
    memory = FloatType(default=0.0)
    is_vm = BooleanType(default=True)
    cpu_model = StringType(default="")
