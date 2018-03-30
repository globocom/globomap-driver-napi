"""
   Copyright 2018 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from .data_spec import DataSpec
from .networkapi import NetworkAPI
from .settings import ACTIONS
from .util import valid_comp_unit_id


class Kind(object):

    def _treat(self, message):
        action = ACTIONS.get(message.get('action'))
        id_object = message.get('data').get('id_object')

        return action, id_object

    def _treat_delete(self, provider, object_id):
        return {'provider': provider, 'id': object_id}

    def _encapsulate(self, action, collection, kind, element):
        data = {
            'action': action,
            'collection': collection,
            'type': kind
        }

        if action != 'DELETE':
            data['element'] = element

        if action != 'CREATE':
            data['key'] = '{}_{}'.format(element['provider'], element['id'])

        return data

    def vip(self, message):
        """Create message of kind VIP"""

        action, id_object = self._treat(message)

        if action != 'DELETE':
            napi = NetworkAPI()
            vip = napi.get_vip(id_object)
            if vip:
                data = DataSpec().vip(vip)
                data['timestamp'] = message.get('timestamp')
            else:
                return []
        else:
            data = self._treat_delete('napi', id_object)

        data_enc = [self._encapsulate(action, 'vip', 'collections', data)]

        return data_enc

    def pool(self, message):
        """Create message of kind Pool"""

        action, id_object = self._treat(message)

        if action != 'DELETE':
            napi = NetworkAPI()
            pool = napi.get_pool(id_object)
            if pool:
                data = DataSpec().pool(pool)
                data['timestamp'] = message.get('timestamp')
            else:
                return []
        else:
            data = self._treat_delete('napi', id_object)

        data_enc = [self._encapsulate(action, 'pool', 'collections', data)]

        return data_enc

    def port(self, message):
        """Create message of kind Port"""

        action, id_object = self._treat(message)

        if action != 'DELETE':
            data = None
            napi = NetworkAPI()
            vip = napi.get_vip_by_portpool_id(id_object)
            if vip:
                for port in vip.get('ports'):
                    for pool in port['pools']:
                        if pool['id'] == id_object:
                            pool['port'] = port['port']
                            pool['options'] = port['options']
                            data = DataSpec().port(pool, port['id'])
                            data['timestamp'] = message.get('timestamp')
                            break
                    else:
                        continue
                    break

            if not data:
                return []
        else:
            data = self._treat_delete('napi', id_object)

        data_enc = [self._encapsulate(action, 'port', 'edges', data)]

        return data_enc

    def comp_unit(self, message):
        """Create message of kind Comp Unit"""

        action, id_object = self._treat(message)

        if action != 'DELETE':
            napi = NetworkAPI()
            equipment = napi.get_equipment(id_object)
            if equipment:
                data = DataSpec().comp_unit(equipment)
                data['timestamp'] = message.get('timestamp')
            else:
                return []
        else:
            name = message['data']['new_value']['nome'].lower()
            compunit_id = valid_comp_unit_id(name)
            data = self._treat_delete('globomap', compunit_id)

        data_enc = [self._encapsulate(
            action, 'comp_unit', 'collections', data)]

        return data_enc

    def pool_comp_unit(self, message):
        """Create message of kind Pool Comp Unit"""

        action, id_object = self._treat(message)
        data = {}

        if action != 'DELETE':
            napi = NetworkAPI()
            pool = napi.get_pool_by_member_id(id_object)
            if pool and pool.get('server_pool_members'):
                for member in pool['server_pool_members']:
                    if member['id'] == id_object:
                        res = DataSpec().pool_comp_unit(member, pool['id'])
                        res['timestamp'] = message.get('timestamp')
                        data.update(res)
                        break
            if not data:
                return []
        else:
            data = self._treat_delete('napi', id_object)

        data_enc = [self._encapsulate(action, 'pool_comp_unit', 'edges', data)]

        return data_enc

    def network_v4_comp_unit(self, message):
        """Create message of kind Network(v4) Comp Unit"""

        action, id_object = self._treat(message)
        data = {}

        if action == 'UPDATE':
            return []

        name = message['data']['new_value']['equipamento']['value'].lower()
        if action == 'CREATE':
            napi = NetworkAPI()
            ipv4 = napi.get_ipv4_by_ip_equipment_id(id_object)
            if ipv4:
                res = DataSpec().network_comp_unit(ipv4, name, id_object)
                res['timestamp'] = message.get('timestamp')
                data.update(res)
            else:
                return []
        else:
            name = 'v4_{}'.format(id_object)
            data = self._treat_delete('napi', name)

        data_enc = [self._encapsulate(
            action, 'network_comp_unit', 'edges', data)]

        return data_enc

    def network_v6_comp_unit(self, message):
        """Create message of kind Network(v6) Comp Unit"""

        action, id_object = self._treat(message)
        data = {}

        if action == 'UPDATE':
            return []

        name = message['data']['new_value']['equipamento']['value'].lower()
        if action == 'CREATE':
            napi = NetworkAPI()
            ipv6 = napi.get_ipv6_by_ip_equipment_id(id_object)
            if ipv6:
                res = DataSpec().network_comp_unit(ipv6, name, id_object)
                res['timestamp'] = message.get('timestamp')
                data.update(res)
            else:
                return []
        else:
            name = 'v6_{}'.format(id_object)
            data = self._treat_delete('napi', name)

        data_enc = [self._encapsulate(
            action, 'network_comp_unit', 'edges', data)]

        return data_enc

    def network_v4(self, message):
        """Create message of kind Network(v4)"""

        action, id_object = self._treat(message)
        data = {}

        if action != 'DELETE':
            napi = NetworkAPI()
            network = napi.get_network_ipv4_id(id_object)
            if network:
                res = DataSpec().network(network)
                res['timestamp'] = message.get('timestamp')
                data.update(res)
            else:
                return []
        else:
            name = 'v4_{}'.format(id_object)
            data = self._treat_delete('napi', name)

        data_enc = [self._encapsulate(action, 'network', 'collections', data)]

        return data_enc

    def network_v6(self, message):
        """Create message of kind Network(v6)"""

        action, id_object = self._treat(message)
        data = {}

        if action != 'DELETE':
            napi = NetworkAPI()
            network = napi.get_network_ipv6_id(id_object)
            if network:
                res = DataSpec().network(network)
                res['timestamp'] = message.get('timestamp')
                data.update(res)
            else:
                return []
        else:
            name = 'v6_{}'.format(id_object)
            data = self._treat_delete('napi', name)

        data_enc = [self._encapsulate(action, 'network', 'collections', data)]

        return data_enc

    def vlan_network_v4(self, message):
        """Create message of kind Vlan Network(v4)"""

        action, id_object = self._treat(message)
        data = {}

        if action != 'DELETE':
            napi = NetworkAPI()
            vlan = napi.get_network_ipv4_id(id_object)
            if vlan:
                res = DataSpec().vlan_network(vlan)
                res['timestamp'] = message.get('timestamp')
                data.update(res)
            else:
                return []
        else:
            name = 'v4_{}'.format(id_object)
            data = self._treat_delete('napi', name)

        data_enc = [self._encapsulate(action, 'vlan_network', 'edges', data)]

        return data_enc

    def vlan_network_v6(self, message):
        """Create message of kind Vlan Network(v6)"""

        action, id_object = self._treat(message)
        data = {}

        if action != 'DELETE':
            napi = NetworkAPI()
            vlan = napi.get_network_ipv6_id(id_object)
            if vlan:
                res = DataSpec().vlan_network(vlan)
                res['timestamp'] = message.get('timestamp')
                data.update(res)
            else:
                return []
        else:
            name = 'v6_{}'.format(id_object)
            data = self._treat_delete('napi', name)

        data_enc = [self._encapsulate(action, 'vlan_network', 'edges', data)]

        return data_enc

    def vlan(self, message):
        """Create message of kind VLAN"""

        action, id_object = self._treat(message)
        data = {}

        if action != 'DELETE':
            napi = NetworkAPI()
            vlan = napi.get_vlan(id_object)
            if vlan:
                res = DataSpec().vlan(vlan)
                res['timestamp'] = message.get('timestamp')
                data.update(res)
            else:
                return []
        else:
            data = self._treat_delete('napi', id_object)

        data_enc = [self._encapsulate(action, 'vlan', 'collections', data)]

        return data_enc

    def environment_vlan(self, message):
        """Create message of kind VLAN"""

        action, id_object = self._treat(message)
        data = {}

        if action != 'DELETE':
            napi = NetworkAPI()
            vlan = napi.get_vlan(id_object)
            if vlan:
                res = DataSpec().environment_vlan(vlan)
                res['timestamp'] = message.get('timestamp')
                data.update(res)
            else:
                return []
        else:
            data = self._treat_delete('napi', id_object)

        data_enc = [self._encapsulate(
            action, 'environment_vlan', 'edges', data)]

        return data_enc

    def environment(self, message):
        """Create message of kind Environment"""

        action, id_object = self._treat(message)
        data = {}

        if action != 'DELETE':
            napi = NetworkAPI()
            environment = napi.get_environment(id_object)
            if environment:
                res = DataSpec().environment(environment)
                res['timestamp'] = message.get('timestamp')
                data.update(res)
            else:
                return []
        else:
            data = self._treat_delete('napi', id_object)

        data_enc = [self._encapsulate(
            action, 'environment', 'collections', data)]

        return data_enc

    def father_environment(self, message):
        """Create message of kind Environment"""

        action, id_object = self._treat(message)
        data = {}

        if action != 'DELETE':
            napi = NetworkAPI()
            environment = napi.get_environment(id_object)
            if environment and environment.get('father_environment'):
                res = DataSpec().father_environment(environment)
                res['timestamp'] = message.get('timestamp')
                data.update(res)
            else:
                return []
        else:
            data = self._treat_delete('napi', id_object)

        data_enc = [self._encapsulate(
            action, 'father_environment', 'edges', data)]

        return data_enc
