from schematics import Model
from schematics.types import StringType, IntType, DictType, ListType
# forwarding Rule
# load_balancer (URL map)
# ...

'''
{
  "id": "projects/bluese-cloudone-20200113/global/urlMaps",
  "items": [
    {
      "id": "1609550378012075925",
      "creationTimestamp": "2020-08-06T21:32:58.747-07:00",
      "name": "dk-https-lb",
      "selfLink": "https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/global/urlMaps/dk-https-lb",
      "defaultService": "https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/global/backendBuckets/dk-test-bucket",
      "fingerprint": "CxT7P-17-1Q=",
      "kind": "compute#urlMap"
    }
  ],
  "selfLink": "https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/global/urlMaps",
  "kind": "compute#urlMapList"
}

'''

'''
{
  "id": "projects/bluese-cloudone-20200113/regions/asia-northeast3/forwardingRules",
  "items": [
    {
      "id": "8813773514932198561",
      "creationTimestamp": "2020-06-17T07:01:50.215-07:00",
      "name": "jhsong-vpn-1-rule-esp",
      "description": "",
      "region": "https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/regions/asia-northeast3",
      "IPAddress": "34.64.88.195",
      "IPProtocol": "ESP",
      "target": "https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/regions/asia-northeast3/targetVpnGateways/jhsong-vpn-1",
      "selfLink": "https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/regions/asia-northeast3/forwardingRules/jhsong-vpn-1-rule-esp",
      "loadBalancingScheme": "EXTERNAL",
      "networkTier": "PREMIUM",
      "fingerprint": "0IYvWh4NwE0=",
      "kind": "compute#forwardingRule"
    },
    {
      "id": "7630047053179493552",
      "creationTimestamp": "2020-06-17T07:02:07.151-07:00",
      "name": "jhsong-vpn-1-rule-udp4500",
      "description": "",
      "region": "https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/regions/asia-northeast3",
      "IPAddress": "34.64.88.195",
      "IPProtocol": "UDP",
      "portRange": "4500-4500",
      "target": "https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/regions/asia-northeast3/targetVpnGateways/jhsong-vpn-1",
      "selfLink": "https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/regions/asia-northeast3/forwardingRules/jhsong-vpn-1-rule-udp4500",
      "loadBalancingScheme": "EXTERNAL",
      "networkTier": "PREMIUM",
      "fingerprint": "W2HpQ86cC_M=",
      "kind": "compute#forwardingRule"
    },
    {
      "id": "5127216086194298041",
      "creationTimestamp": "2020-06-17T07:01:58.618-07:00",
      "name": "jhsong-vpn-1-rule-udp500",
      "description": "",
      "region": "https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/regions/asia-northeast3",
      "IPAddress": "34.64.88.195",
      "IPProtocol": "UDP",
      "portRange": "500-500",
      "target": "https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/regions/asia-northeast3/targetVpnGateways/jhsong-vpn-1",
      "selfLink": "https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/regions/asia-northeast3/forwardingRules/jhsong-vpn-1-rule-udp500",
      "loadBalancingScheme": "EXTERNAL",
      "networkTier": "PREMIUM",
      "fingerprint": "SC7Ll2OXYZQ=",
      "kind": "compute#forwardingRule"
    }
  ],
  "selfLink": "https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/regions/asia-northeast3/forwardingRules",
  "kind": "compute#forwardingRuleList"
}

'''
class LoadBalancer(Model):
    type = StringType(choices=('application', 'network'))
    name = StringType()
    dns = StringType()
    port = ListType(IntType())
    protocol = ListType(StringType())
    scheme = StringType(choices=('internet-facing', 'internal'))
    tags = DictType(StringType, default={})
