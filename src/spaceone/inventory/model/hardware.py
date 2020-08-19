from schematics import Model
from schematics.types import IntType, FloatType, StringType, ListType, BooleanType, DateType


class Hardware(Model):
    core = IntType(default=0)
    memory = FloatType(default=0.0)
    memory_count = IntType(default=0, serialize_when_none=False)
    manufacturer = StringType(serialize_when_none=False)
    model = StringType(serialize_when_none=False)
    serial_number = StringType(serialize_when_none=False)
    cpu_model = ListType(default=[])
    threads_per_core = IntType(default=0, serialize_when_none=False)
    core_per_socket = IntType(default=0, serialize_when_none=False)
    cpu_socket = IntType(default=0, serialize_when_none=False)
    cpu_arch = StringType(serialize_when_none=False)
    hyperthreading =  BooleanType(default=False, serialize_when_none=False)
    bios_version = StringType(serialize_when_none=False)
    bios_release_at = DateType(serialize_when_none=False)
    is_vm = StringType(serialize_when_none=False)

    # get_instance_type =
'''
{
  "id": "projects/bluese-cloudone-20200113/zones/asia-northeast3-a/machineTypes",
  "items": [
    {
      "id": "337016",
      "creationTimestamp": "1969-12-31T16:00:00.000-08:00",
      "name": "e2-highcpu-16",
      "description": "Efficient Instance, 16 vCPUs, 16 GB RAM",
      "guestCpus": 16,
      "memoryMb": 16384,
      "maximumPersistentDisks": 128,
      "maximumPersistentDisksSizeGb": "263168",
      "zone": "asia-northeast3-a",
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/machineTypes/e2-highcpu-16",
      "isSharedCpu": false,
      "kind": "compute#machineType"
    },
'''