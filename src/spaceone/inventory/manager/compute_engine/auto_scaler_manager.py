from spaceone.core.manager import BaseManager
from spaceone.inventory.model.auto_scaler import AutoScaler
'''
{
  "id": "projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instanceGroups",
  "items": [
    {
      "id": "4591700184858139551",
      "creationTimestamp": "2020-08-19T06:13:20.345-07:00",
      "name": "instance-group-1",
      "description": "This instance group is controlled by Instance Group Manager 'instance-group-1'. To modify instances in this group, use the Instance Group Manager API: https://cloud.google.com/compute/docs/reference/latest/instanceGroupManagers",
      "network": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/global/networks/default",
      "fingerprint": "42WmSpB8rSM=",
      "zone": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a",
      "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instanceGroups/instance-group-1",
      "size": 1,
      "subnetwork": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/regions/asia-northeast3/subnetworks/default",
      "kind": "compute#instanceGroup"
    }
  ],
  "selfLink": "https://www.googleapis.com/compute/beta/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instanceGroups",
  "kind": "compute#instanceGroupList"
}



'''

class AutoScalerManager(BaseManager):

    def __init__(self, params, vm_connector=None):
        self.params = params
        self.vm_connector = vm_connector

    def get_auto_scaler_info(self, instance_id, auto_scalers):
        '''
        auto_scaler_data = {
            name: '',
            id: '',
            self_link: '',
            'instance_group': {
                'id': '',
                'name': ''
                'self_link': ''
                'instance_template_name': ''
            }
        }
        '''

        auto_scaler_data = {}
        match_autoscaling_group = self.get_auto_scaling_group_from_instance_id(instance_id, auto_scalers)

        if match_autoscaling_group is not None:
            auto_scaler_data = {
                'name': match_autoscaling_group.get('AutoScalingGroupName', ''),
                'id': match_autoscaling_group.get('AutoScalingGroupARN', ''),
                'id': match_autoscaling_group.get('AutoScalingGroupARN', ''),
            }

            return AutoScaler(auto_scaler_data, strict=False)
        else:
            return None

    def get_auto_scaling_group_from_instance_id(self, instance_id, auto_scalers):
        match_auto_scaling_group = None
        match_launch_configuration = None
        match_lc_name = None

        for single_auto_scaler in auto_scalers:
            target = single_auto_scaler.get('target')



        return match_auto_scaling_group, match_launch_configuration
