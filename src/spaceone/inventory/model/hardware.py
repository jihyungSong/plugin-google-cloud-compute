from schematics import Model
from schematics.types import IntType, FloatType, StringType, ListType, BooleanType, DateType

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


class Hardware(Model):
    core = IntType(default=0)
    memory = FloatType(default=0.0)
    is_vm = StringType(default=True)
    cpu_model = ListType(StringType(default=""))

    # get_instance_type =
