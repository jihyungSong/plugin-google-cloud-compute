from spaceone.core.manager import BaseManager
from spaceone.inventory.model.auto_scaler import AutoScaler
class AutoScalerManager(BaseManager):
    def __init__(self):
        pass

    def get_auto_scaler_info(self, instance, instance_group_managers, auto_scalers):
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
        matched_inst_group = self.get_matched_instance_group(instance, instance_group_managers)
        auto_scaler_data = self._get_auto_scaler_data(matched_inst_group, auto_scalers)

        if auto_scaler_data is not None:
            return AutoScaler(auto_scaler_data, strict=False)
        else:
            return None

    def get_matched_instance_group(self, instance, instance_groups):
        matched_instance_group = None
        for instance_group in instance_groups:
            find = False
            instance_list = instance_group.get('instance_list', [])
            for single_inst in instance_list:
                instance_name = self._get_key_name('instance', single_inst)
                if instance.get('name') == instance_name:
                    matched_instance_group = instance_group
                    find = True
                    break
            if find:
                break

        return matched_instance_group

    @staticmethod
    def _get_auto_scaler_data(matched_inst_group, auto_scalers):
        auto_scaler_data = None
        if matched_inst_group is not None:
            for auto_scaler in auto_scalers:
                auto_scaler_self_link = auto_scaler.get('selfLink', '')
                matched_status = matched_inst_group.get('status', {})
                if auto_scaler_self_link == matched_status.get('autoscaler', ''):
                    auto_scaler_data = {
                        'name': auto_scaler.get('name', ''),
                        'id': auto_scaler.get('id', ''),
                        'self_link': auto_scaler.get('selfLink', ''),
                        'instance_group': {
                            'id': matched_inst_group.get('id', ''),
                            'name': matched_inst_group.get('name', ''),
                            'self_link': matched_inst_group.get('selfLink', ''),
                            'instance_template_name': matched_inst_group.get('instanceTemplate', ''),
                        }
                    }
                    break
        return auto_scaler_data

    @staticmethod
    def _get_key_name(key, self_link_source):
        instance_self_link = self_link_source.get(key, '')
        instance_self_link_split = instance_self_link.split('/')
        return instance_self_link_split[-1]