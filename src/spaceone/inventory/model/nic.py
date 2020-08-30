from schematics import Model
from schematics.types import StringType, IntType, ListType, DictType

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

class NIC(Model):
    device_index = IntType()                    # ok
    device = StringType(default="")
    cidr = StringType()
    nic_type = StringType(default="Virtual")    # 확인 필요
    ip_addresses = ListType(StringType())       # 확인필요 (accessConfig)
    mac_address = StringType(default="")
    public_ip_address = StringType()
    tags = DictType(StringType, default={})
