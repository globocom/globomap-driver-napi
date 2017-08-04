from .data_spec import DataSpec
from .networkapi import NetworkAPI
from .settings import ACTIONS


class Kind(object):

    def _treat(self, message):
        action = ACTIONS.get(message.get('action'))
        id_object = message.get('data').get('id_object')

        return action, id_object

    def _encapsulate(self, action, collection, kind, data):
        data = {
            'action': action,
            'collection': collection,
            'type': kind,
            'element': data,
        }

        return data

    def vip(self, message):
        action, id_object = self._treat(message)
        data = {}

        if action != 'DELETE':
            napi = NetworkAPI()
            vip = napi.get_vip(id_object)
            if vip:
                res = DataSpec().vip(vip)
                res['timestamp'] = message['timestamp']
                data.update(res)
            else:
                return False

        if action != 'CREATE':
            data['key'] = 'vip/napi_{}'.format(id_object)

        data = self._encapsulate(action, 'vip', 'collections', data)

        return data

    def pool(self, message):
        action, id_object = self._treat(message)
        data = {}

        if action != 'DELETE':
            napi = NetworkAPI()
            pool = napi.get_pool(id_object)
            if pool:
                res = DataSpec().pool(pool)
                res['timestamp'] = message['timestamp']
                data.update(res)
            else:
                return False

        if action != 'CREATE':
            data['key'] = 'pool/napi_{}'.format(id_object)

        data = self._encapsulate(action, 'pool', 'collections', data)

        return data

    def port(self, message):
        action, id_object = self._treat(message)
        data = {}

        if action != 'DELETE':
            napi = NetworkAPI()
            vip = napi.get_vip_by_portpool_id(id_object)
            if vip:
                for port in vip['ports']:
                    for pool in port['pools']:
                        if pool['id'] == id_object:
                            pool['port'] = port['port']
                            res = DataSpec().port(pool, port['id'])
                            res['timestamp'] = message['timestamp']
                            data.update(res)
                            break
                    else:
                        continue
                    break

            if not data:
                return False

        if action != 'CREATE':
            data['key'] = 'port/napi_{}'.format(id_object)

        data = self._encapsulate(action, 'port', 'edges', data)

        return data

    # def comp_unit(self, message):
    #     action, id_object = self._treat(message)

    #     data = {}
    #     if action != 'CREATE':
    #         data = {
    #             'key': 'comp_unit/globomap_{}'.format(message['data']['name'])
    #         }

    #     if action != 'DELETE':
    #         data["timestamp"] = message["timestamp"]

    #         napi = NetworkAPI()
    #         pool = napi.get_pool_by_member_id(id_object)

    #         for member in pool['server_pool_members']:
    #             if member['id'] == id_object:
    #                 eqpt = member['equipment']
    #                 res = DataSpec().comp_unit(eqpt)
    #                 data.update(res)

    #     data = self._encapsulate(action, 'comp_unit', 'collections', data)

    #     return data

    def pool_comp_unit(self, message):
        action, id_object = self._treat(message)
        data = {}

        if action != 'DELETE':
            napi = NetworkAPI()
            pool = napi.get_pool_by_member_id(id_object)
            if pool:
                for member in pool['server_pool_members']:
                    if member['id'] == id_object:
                        res = DataSpec().pool_comp_unit(member, pool['id'])
                        res['timestamp'] = message['timestamp']
                        data.update(res)
                        break
            if not data:
                return False

        if action != 'CREATE':
            data['key'] = 'pool_comp_unit/napi_{}'.format(id_object)

        data = self._encapsulate(action, 'pool_comp_unit', 'edges', data)

        return data
