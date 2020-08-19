from schematics import Model
from schematics.types import StringType, IntType, ListType, ModelType

'''
 "networkInterfaces": [
        {
          "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
          "subnetwork": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast3/subnetworks/default",
          "networkIP": "10.178.0.60",
          "name": "nic0",
          "accessConfigs": [
            {
              "type": "ONE_TO_ONE_NAT",
              "name": "External NAT",
              "natIP": "34.64.165.120",
              "networkTier": "PREMIUM",
              "kind": "compute#accessConfig"
            }
          ],
          "fingerprint": "8oG0qiOfFgc=",
          "kind": "compute#networkInterface"
        }
      ]
'''

class NICTags(Model):
    public_dns = StringType(serialize_when_none=False)

class NIC(Model):
    device_index = IntType() #ok
    device = StringType(default="")
    # subnetwork 로 해서 찾아와야 함
    cidr = StringType()

    nic_type = StringType()
    ip_addresses = ListType(StringType()) #ok

    mac_address = StringType() # couldn't find one yet
    public_ip_address = StringType() #if setup on VPC is availble can get
    tags = ModelType(NICTags, default={})
