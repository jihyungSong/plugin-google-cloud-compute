from schematics import Model
from schematics.types import StringType, IntType, FloatType, BooleanType, ModelType, DictType

'''
{
  "id": "3358936943321049290",
  "creationTimestamp": "2020-08-18T06:22:45.863-07:00",
  "name": "dk-test-attached-081820",
  "description": "dk-test-attached-081820",
  "sizeGb": "10",
  "zone": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a",
  "status": "READY",
  "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/disks/dk-test-attached-081820",
  "type": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/diskTypes/pd-balanced",
  "lastAttachTimestamp": "2020-08-18T06:22:57.405-07:00",
  "users": [
    "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instances/js-test"
  ],
  "labels": {
    "name": "dk_created_as"
  },
  "labelFingerprint": "g8kd3RSB8Ug=",
  "physicalBlockSizeBytes": "4096",
  "interface": "SCSI",
  "kind": "compute#disk"
}
'''


class DiskTags(Model):
    disk_id = StringType(serialize_when_none=False)
    disk_name = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    zone = StringType(serialize_when_none=False)
    disk_type = StringType(choices=('local-ssd', 'pd-balanced', 'pd-ssd', 'pd-standard'), serialize_when_none=False)
    encrypted = BooleanType(default=True)
    read_iops = FloatType(serialize_when_none=False)
    write_iops = FloatType(serialize_when_none=False)
    labels = DictType(serialize_when_none=False)


class Disk(Model):
    device_index = IntType()
    device = StringType(default="")
    disk_type = StringType(default="disk")
    size = FloatType()
    tags = ModelType(DiskTags, default={})
