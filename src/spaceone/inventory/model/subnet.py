from schematics import Model
from schematics.types import StringType
'''
{
  "items": [
    {
      "id": "5028091457940084154",
      "creationTimestamp": "2020-01-13T05:06:29.378-08:00",
      "name": "default",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
      "ipCidrRange": "10.178.0.0/20",
      "gatewayAddress": "10.178.0.1",
      "region": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast3",
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast3/subnetworks/default",
      "privateIpGoogleAccess": false,
      "fingerprint": "bvkW3drQF1Y=",
      "allowSubnetCidrRoutesOverlap": false,
      "purpose": "PRIVATE",
      "kind": "compute#subnetwork"
    }
}

'''

class SubnetWork(Model):
    subnet_id = StringType()
    cidr = StringType()
    subnet_name = StringType()
