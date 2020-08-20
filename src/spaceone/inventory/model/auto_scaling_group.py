from schematics import Model
from schematics.types import StringType, ModelType
'''
{
  "id": "projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instanceGroupManagers",
  "items": [
    {
      "id": "4480862519355808671",
      "creationTimestamp": "2020-08-19T06:13:20.334-07:00",
      "name": "instance-group-1",
      "zone": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a",
      "instanceTemplate": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/instanceTemplates/jhsong-template-1",
      "versions": [
        {
          "instanceTemplate": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/instanceTemplates/jhsong-template-1",
          "targetSize": {
            "calculated": 1
          }
        }
      ],
      "instanceGroup": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instanceGroups/instance-group-1",
      "baseInstanceName": "instance-group-1",
      "fingerprint": "E-AO4W7HWDs=",
      "currentActions": {
        "none": 1,
        "creating": 0,
        "creatingWithoutRetries": 0,
        "verifying": 0,
        "recreating": 0,
        "deleting": 0,
        "abandoning": 0,
        "restarting": 0,
        "refreshing": 0
      },
      "status": {
        "isStable": true,
        "versionTarget": {
          "isReached": true
        },
        "stateful": {
          "isStateful": false,
          "hasStatefulConfig": false,
          "perInstanceConfigs": {
            "allEffective": true
          }
        },
        "autoscaler": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/autoscalers/instance-group-1"
      },
      "targetSize": 1,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instanceGroupManagers/instance-group-1",
      "autoHealingPolicies": [
        {
          "healthCheck": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/healthChecks/jhsong-check",
          "initialDelaySec": 300
        }
      ],
      "updatePolicy": {
        "type": "OPPORTUNISTIC",
        "minimalAction": "REPLACE",
        "maxSurge": {
          "fixed": 1,
          "calculated": 1
        },
        "maxUnavailable": {
          "fixed": 1,
          "calculated": 1
        },
        "minReadySec": 0,
        "replacementMethod": "SUBSTITUTE"
      },
      "serviceAccount": "286919713412@cloudservices.gserviceaccount.com",
      "kind": "compute#instanceGroupManager"
    }
  ],
  "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instanceGroupManagers",
  "kind": "compute#instanceGroupManagerList"
}

{
  "id": "projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instanceGroupManagers",
  "items": [
    {
      "id": "4480862519355808671",
      "creationTimestamp": "2020-08-19T06:13:20.334-07:00",
      "name": "instance-group-1",
      "zone": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a",
      "instanceTemplate": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/instanceTemplates/jhsong-template-1",
      "versions": [
        {
          "instanceTemplate": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/instanceTemplates/jhsong-template-1",
          "targetSize": {
            "calculated": 1
          }
        }
      ],
      "instanceGroup": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instanceGroups/instance-group-1",
      "baseInstanceName": "instance-group-1",
      "fingerprint": "E-AO4W7HWDs=",
      "currentActions": {
        "none": 1,
        "creating": 0,
        "creatingWithoutRetries": 0,
        "verifying": 0,
        "recreating": 0,
        "deleting": 0,
        "abandoning": 0,
        "restarting": 0,
        "refreshing": 0
      },
      "status": {
        "isStable": true,
        "versionTarget": {
          "isReached": true
        },
        "stateful": {
          "isStateful": false,
          "hasStatefulConfig": false,
          "perInstanceConfigs": {
            "allEffective": true
          }
        },
        "autoscaler": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/autoscalers/instance-group-1"
      },
      "targetSize": 1,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instanceGroupManagers/instance-group-1",
      "autoHealingPolicies": [
        {
          "healthCheck": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/healthChecks/jhsong-check",
          "initialDelaySec": 300
        }
      ],
      "updatePolicy": {
        "type": "OPPORTUNISTIC",
        "minimalAction": "REPLACE",
        "maxSurge": {
          "fixed": 1,
          "calculated": 1
        },
        "maxUnavailable": {
          "fixed": 1,
          "calculated": 1
        },
        "minReadySec": 0,
        "replacementMethod": "SUBSTITUTE"
      },
      "serviceAccount": "286919713412@cloudservices.gserviceaccount.com",
      "kind": "compute#instanceGroupManager"
    },
    {
      "id": "6101888785817048759",
      "creationTimestamp": "2020-08-19T06:25:44.421-07:00",
      "name": "instance-group-dk-2",
      "description": "instance-group-dk-2",
      "zone": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a",
      "instanceTemplate": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/instanceTemplates/jhsong-template-1",
      "versions": [
        {
          "instanceTemplate": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/instanceTemplates/jhsong-template-1",
          "targetSize": {
            "calculated": 1
          }
        }
      ],
      "instanceGroup": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instanceGroups/instance-group-dk-2",
      "baseInstanceName": "instance-group-dk-2",
      "fingerprint": "5NgF5yp4FvY=",
      "currentActions": {
        "none": 1,
        "creating": 0,
        "creatingWithoutRetries": 0,
        "verifying": 0,
        "recreating": 0,
        "deleting": 0,
        "abandoning": 0,
        "restarting": 0,
        "refreshing": 0
      },
      "status": {
        "isStable": true,
        "versionTarget": {
          "isReached": true
        },
        "stateful": {
          "isStateful": false,
          "hasStatefulConfig": false,
          "perInstanceConfigs": {
            "allEffective": true
          }
        },
        "autoscaler": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/autoscalers/instance-group-dk-2"
      },
      "targetSize": 1,
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instanceGroupManagers/instance-group-dk-2",
      "updatePolicy": {
        "type": "OPPORTUNISTIC",
        "minimalAction": "REPLACE",
        "maxSurge": {
          "fixed": 1,
          "calculated": 1
        },
        "maxUnavailable": {
          "fixed": 1,
          "calculated": 1
        },
        "minReadySec": 0,
        "replacementMethod": "SUBSTITUTE"
      },
      "serviceAccount": "286919713412@cloudservices.gserviceaccount.com",
      "kind": "compute#instanceGroupManager"
    }
  ],
  "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instanceGroupManagers",
  "kind": "compute#instanceGroupManagerList"
}

'''
# 인스턴스 템플릿
# 인스턴스 그룹
class InstanceTemplate(Model):
    name = StringType()


class InstanceGroup(Model):
    name = StringType()

#Autoscaling
#Autoscaling_mode

'''
By Metric
CPU
Loadblancer
StackDrive
'''

class AutoScalingGroup(Model):
    name = StringType()
    instance_template = ModelType(InstanceTemplate, serialize_when_none=False)
    instance_group = ModelType(InstanceGroup, serialize_when_none=False)
