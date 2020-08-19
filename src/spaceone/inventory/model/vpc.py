from schematics import Model
from schematics.types import StringType

'''
{
  "id": "projects/bluese-cloudone-20200113/global/networks",
  "items": [
    {
      "id": "5250957968059502670",
      "creationTimestamp": "2020-01-13T00:47:29.285-08:00",
      "name": "default",
      "description": "Default network for the project",
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
      "autoCreateSubnetworks": true,
      "subnetworks": [
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast2/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/us-west2/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/us-east4/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/europe-west3/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/northamerica-northeast1/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-southeast2/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/australia-southeast1/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/us-central1/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-southeast1/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/us-east1/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/us-west1/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/southamerica-east1/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-south1/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/europe-west4/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/us-west3/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-east2/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/us-west4/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/europe-north1/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-east1/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast1/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/europe-west2/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/europe-west6/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast3/subnetworks/default",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/europe-west1/subnetworks/default"
      ],
      "routingConfig": {
        "routingMode": "REGIONAL"
      },
      "kind": "compute#network"
    },
    {
      "id": "6293010041599492958",
      "creationTimestamp": "2020-08-06T19:34:25.860-07:00",
      "name": "dk-test-vpc-network-01",
      "description": "dk-test-vpc-network",
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/dk-test-vpc-network-01",
      "autoCreateSubnetworks": false,
      "subnetworks": [
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast3/subnetworks/dk-test3",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast2/subnetworks/dk-test2",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast1/subnetworks/dk-test1"
      ],
      "routingConfig": {
        "routingMode": "REGIONAL"
      },
      "kind": "compute#network"
    },
    {
      "id": "7015047104059713299",
      "creationTimestamp": "2020-05-05T00:47:08.414-07:00",
      "name": "jhsong-test",
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/jhsong-test",
      "autoCreateSubnetworks": false,
      "subnetworks": [
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast1/subnetworks/jhsong-subnet-01",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast3/subnetworks/jhsong-subnet-03",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast2/subnetworks/jhsong-subnet-02"
      ],
      "routingConfig": {
        "routingMode": "REGIONAL"
      },
      "kind": "compute#network"
    },
    {
      "id": "6197243343307679562",
      "creationTimestamp": "2020-01-27T18:17:09.182-08:00",
      "name": "spaceone-dev",
      "description": "spaceone dev vpc",
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/spaceone-dev",
      "autoCreateSubnetworks": false,
      "subnetworks": [
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast3/subnetworks/spaceone-dev-db-a",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast3/subnetworks/spaceone-dev-public-b",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast3/subnetworks/spaceone-dev-private-a",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast3/subnetworks/spaceone-dev-private-b",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast3/subnetworks/spaceone-dev-db-b",
        "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast3/subnetworks/spaceone-dev-public-a"
      ],
      "routingConfig": {
        "routingMode": "REGIONAL"
      },
      "kind": "compute#network"
    }
  ],
  "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks",
  "kind": "compute#networkList"
}
'''

class VPC(Model):
    vpc_id = StringType()
    vpc_name = StringType(default="")
    description = StringType(default="")
    self_link = StringType(default="")
