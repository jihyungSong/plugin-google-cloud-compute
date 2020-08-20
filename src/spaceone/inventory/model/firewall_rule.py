from schematics import Model
from schematics.types import StringType, IntType

#Firewall
'''
{
  "id": "projects/bluese-cloudone-20200113/global/firewalls",
  "items": [
    {
      "id": "7093361134006336416",
      "creationTimestamp": "2020-05-04T00:33:35.648-07:00",
      "name": "allow-all-jinsu",
      "description": "jinsu",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
      "priority": 1000,
      "sourceRanges": [
        "0.0.0.0/0"
      ],
      "targetTags": [
        "allow-all-instance"
      ],
      "allowed": [
        {
          "IPProtocol": "tcp"
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/allow-all-jinsu",
      "kind": "compute#firewall"
    },
    {
      "id": "2926844575987615609",
      "creationTimestamp": "2020-01-22T17:40:38.615-08:00",
      "name": "default-allow-http",
      "description": "",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
      "priority": 1000,
      "sourceRanges": [
        "0.0.0.0/0"
      ],
      "targetTags": [
        "http-server"
      ],
      "allowed": [
        {
          "IPProtocol": "tcp",
          "ports": [
            "80"
          ]
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/default-allow-http",
      "kind": "compute#firewall"
    },
    {
      "id": "5163553416487978872",
      "creationTimestamp": "2020-01-22T17:40:39.099-08:00",
      "name": "default-allow-https",
      "description": "",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
      "priority": 1000,
      "sourceRanges": [
        "0.0.0.0/0"
      ],
      "targetTags": [
        "https-server"
      ],
      "allowed": [
        {
          "IPProtocol": "tcp",
          "ports": [
            "443"
          ]
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/default-allow-https",
      "kind": "compute#firewall"
    },
    {
      "id": "9211567931286196270",
      "creationTimestamp": "2020-01-13T00:48:01.237-08:00",
      "name": "default-allow-icmp",
      "description": "Allow ICMP from anywhere",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
      "priority": 65534,
      "sourceRanges": [
        "0.0.0.0/0"
      ],
      "allowed": [
        {
          "IPProtocol": "icmp"
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/default-allow-icmp",
      "kind": "compute#firewall"
    },
    {
      "id": "6182791667417976878",
      "creationTimestamp": "2020-01-13T00:48:01.211-08:00",
      "name": "default-allow-internal",
      "description": "Allow internal traffic on the default network",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
      "priority": 65534,
      "sourceRanges": [
        "10.128.0.0/9"
      ],
      "allowed": [
        {
          "IPProtocol": "tcp",
          "ports": [
            "0-65535"
          ]
        },
        {
          "IPProtocol": "udp",
          "ports": [
            "0-65535"
          ]
        },
        {
          "IPProtocol": "icmp"
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/default-allow-internal",
      "kind": "compute#firewall"
    },
    {
      "id": "4622023624615890990",
      "creationTimestamp": "2020-01-13T00:48:01.228-08:00",
      "name": "default-allow-rdp",
      "description": "Allow RDP from anywhere",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
      "priority": 65534,
      "sourceRanges": [
        "0.0.0.0/0"
      ],
      "allowed": [
        {
          "IPProtocol": "tcp",
          "ports": [
            "3389"
          ]
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/default-allow-rdp",
      "kind": "compute#firewall"
    },
    {
      "id": "7531392766793846830",
      "creationTimestamp": "2020-01-13T00:48:01.220-08:00",
      "name": "default-allow-ssh",
      "description": "Allow SSH from anywhere",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
      "priority": 65534,
      "sourceRanges": [
        "0.0.0.0/0"
      ],
      "allowed": [
        {
          "IPProtocol": "tcp",
          "ports": [
            "22"
          ]
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/default-allow-ssh",
      "kind": "compute#firewall"
    },
    {
      "id": "7051857872892080627",
      "creationTimestamp": "2020-06-18T08:58:20.816-07:00",
      "name": "jhsong-sg",
      "description": "",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/jhsong-test",
      "priority": 1000,
      "sourceRanges": [
        "172.16.0.0/16"
      ],
      "allowed": [
        {
          "IPProtocol": "all"
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/jhsong-sg",
      "kind": "compute#firewall"
    },
    {
      "id": "5405506207215923527",
      "creationTimestamp": "2020-06-18T09:00:40.389-07:00",
      "name": "jhsong-ssh",
      "description": "",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/jhsong-test",
      "priority": 1000,
      "sourceRanges": [
        "0.0.0.0/0"
      ],
      "allowed": [
        {
          "IPProtocol": "all"
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/jhsong-ssh",
      "kind": "compute#firewall"
    },
    {
      "id": "6397669684409781578",
      "creationTimestamp": "2020-08-05T01:53:57.365-07:00",
      "name": "jhsong-test",
      "description": "",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
      "priority": 1000,
      "sourceRanges": [
        "0.0.0.0/0"
      ],
      "targetTags": [
        "jhsong-test"
      ],
      "allowed": [
        {
          "IPProtocol": "tcp",
          "ports": [
            "8080"
          ]
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/jhsong-test",
      "kind": "compute#firewall"
    },
    {
      "id": "4642321876294028570",
      "creationTimestamp": "2020-08-05T01:55:17.678-07:00",
      "name": "jhsong-test-02",
      "description": "",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
      "priority": 1100,
      "sourceTags": [
        "jhsong-test"
      ],
      "allowed": [
        {
          "IPProtocol": "tcp",
          "ports": [
            "8080"
          ]
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/jhsong-test-02",
      "kind": "compute#firewall"
    },
    {
      "id": "4975422939712711869",
      "creationTimestamp": "2020-02-17T00:44:02.469-08:00",
      "name": "k8s-66aeffffb9e3b4d9-node-http-hc",
      "description": "{\"kubernetes.io/cluster-id\":\"66aeffffb9e3b4d9\"}",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/spaceone-dev",
      "priority": 1000,
      "sourceRanges": [
        "130.211.0.0/22",
        "35.191.0.0/16",
        "209.85.152.0/22",
        "209.85.204.0/22"
      ],
      "targetTags": [
        "gke-spaceone-test-cluster-36518c73-node"
      ],
      "allowed": [
        {
          "IPProtocol": "tcp",
          "ports": [
            "10256"
          ]
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/k8s-66aeffffb9e3b4d9-node-http-hc",
      "kind": "compute#firewall"
    },
    {
      "id": "3405263598729874763",
      "creationTimestamp": "2020-03-17T18:04:36.498-07:00",
      "name": "k8s-817896f5a66e0308-node-http-hc",
      "description": "{\"kubernetes.io/cluster-id\":\"817896f5a66e0308\"}",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
      "priority": 1000,
      "sourceRanges": [
        "35.191.0.0/16",
        "209.85.152.0/22",
        "209.85.204.0/22",
        "130.211.0.0/22"
      ],
      "targetTags": [
        "gke-spaceone-cluster-bf308bba-node"
      ],
      "allowed": [
        {
          "IPProtocol": "tcp",
          "ports": [
            "10256"
          ]
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/k8s-817896f5a66e0308-node-http-hc",
      "kind": "compute#firewall"
    },
    {
      "id": "3507294687194828145",
      "creationTimestamp": "2020-03-17T18:04:30.658-07:00",
      "name": "k8s-fw-a6000846e68b411ea94af42010ab2004",
      "description": "{\"kubernetes.io/service-name\":\"istio-system/istio-ingressgateway\", \"kubernetes.io/service-ip\":\"34.64.93.222\"}",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
      "priority": 1000,
      "sourceRanges": [
        "0.0.0.0/0"
      ],
      "targetTags": [
        "gke-spaceone-cluster-bf308bba-node"
      ],
      "allowed": [
        {
          "IPProtocol": "tcp",
          "ports": [
            "15020",
            "80",
            "443",
            "31400",
            "15029",
            "15030",
            "15031",
            "15032",
            "15443"
          ]
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/k8s-fw-a6000846e68b411ea94af42010ab2004",
      "kind": "compute#firewall"
    },
    {
      "id": "7435108881445416100",
      "creationTimestamp": "2020-02-17T00:43:55.311-08:00",
      "name": "k8s-fw-a894c4dea516111ea8a1342010ab2007",
      "description": "{\"kubernetes.io/service-name\":\"istio-system/istio-ingressgateway\", \"kubernetes.io/service-ip\":\"34.64.102.91\"}",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/spaceone-dev",
      "priority": 1000,
      "sourceRanges": [
        "0.0.0.0/0"
      ],
      "targetTags": [
        "gke-spaceone-test-cluster-36518c73-node"
      ],
      "allowed": [
        {
          "IPProtocol": "tcp",
          "ports": [
            "15020",
            "80",
            "443",
            "31400",
            "15029",
            "15030",
            "15031",
            "15032",
            "15443"
          ]
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/k8s-fw-a894c4dea516111ea8a1342010ab2007",
      "kind": "compute#firewall"
    },
    {
      "id": "6181661880569293978",
      "creationTimestamp": "2020-02-17T00:44:37.992-08:00",
      "name": "k8s-fw-a8d4ea7ec516111ea8a1342010ab2007",
      "description": "{\"kubernetes.io/service-name\":\"gke-system/istio-ingress\", \"kubernetes.io/service-ip\":\"34.64.81.96\"}",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/spaceone-dev",
      "priority": 1000,
      "sourceRanges": [
        "0.0.0.0/0"
      ],
      "targetTags": [
        "gke-spaceone-test-cluster-36518c73-node"
      ],
      "allowed": [
        {
          "IPProtocol": "tcp",
          "ports": [
            "15020",
            "80",
            "443"
          ]
        }
      ],
      "direction": "INGRESS",
      "enableLogging": false,
      "logConfig": {
        "enable": false
      },
      "disabled": false,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls/k8s-fw-a8d4ea7ec516111ea8a1342010ab2007",
      "kind": "compute#firewall"
    }
  ],
  "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/firewalls",
  "kind": "compute#firewallList"
}
'''


class FirewallRule(Model):
    priority = IntType(serialize_when_none=False)
    protocol = StringType()
    remote = StringType()                                   # mimic
    remote_id = StringType(serialize_when_none=False)       # filter value
    remote_cidr = StringType(serialize_when_none=False)     # cidr
    security_group_name = StringType(default="")
    port_range_min = IntType(serialize_when_none=False)
    port_range_max = IntType(serialize_when_none=False)
    security_group_id = StringType()
    description = StringType(default="")
    direction = StringType(choices=("inboud", "outbound"))
    port = StringType(serialize_when_none=False)
    action = StringType(choices=('allow', 'deny'))
