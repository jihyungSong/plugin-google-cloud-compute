from spaceone.core.manager import BaseManager
from spaceone.inventory.model.auto_scaler import AutoScaler


class AutoScalerManager(BaseManager):
    def __init__(self, params, vm_connector=None):
        self.params = params
        self.vm_connector = vm_connector

    def get_auto_scaler_info(self, instance, instance_groups, auto_scalers):
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
        matched_inst_group = self.get_auto_scaler_from_instance(self, instance, instance_groups)
        auto_scaler_data = self._get_auto_scaler_data(matched_inst_group, auto_scalers)
        if auto_scaler_data is not None:
            return AutoScaler(auto_scaler_data, strict=False)
        else:
            return None


    def get_matched_instance_group(self, instance, instance_groups):
        matched_instance_group = None
        for instance_group in instance_groups:
            find = False
            instance_group_name = instance_group.get('baseInstanceName', '')
            inst_list = self.vm_connector.list_instance_from_instance_group(instance_group_name)
            for single_in_inst_list in inst_list:
                instance_name = self._get_key_name('instance', single_in_inst_list)
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
                if auto_scaler_self_link == matched_inst_group.get('autoscaler', ''):
                    auto_scaler_data = {
                        'name': auto_scaler.get('name', ''),
                        'id': auto_scaler.get('id', ''),
                        'self_link': auto_scaler.get('selfLink', ''),
                        'instance_group': {
                            'id': matched_inst_group.get('id', ''),
                            'name': matched_inst_group.get('name', ''),
                            'self_link': matched_inst_group.get('self_link', ''),
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