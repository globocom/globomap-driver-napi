from .data_spec import DataSpec
from .networkapi import NetworkAPI


class Kind(object):

    def vip(self, id_object):
        napi = NetworkAPI()
        vip = napi.get_vip(id_object)

        data = DataSpec().vip(vip)
        return data

    def pool(self, id_object):

        napi = NetworkAPI()
        pool = napi.get_pool(id_object)

        data = DataSpec().pool(pool)
        return data

    def port(self, id_object):

        napi = NetworkAPI()
        vip = napi.get_vip_by_portpool_id(id_object)

        data = None
        for port in vip['ports']:
            for pool in port['pools']:
                if pool['id'] == id_object:
                    pool['port'] = port['port']
                    data = DataSpec().port(pool, port['id'])
        return data

    def comp_unit(self, id_object):

        napi = NetworkAPI()
        pool = napi.get_pool_by_member_id(id_object)

        data = None
        for member in pool['server_pool_members']:
            if member['id'] == id_object:
                eqpt = member['equipment']
                data = DataSpec().comp_unit(eqpt)
        return data

    def pool_comp_unit(self, id_object):
        napi = NetworkAPI()
        pool = napi.get_pool_by_member_id(id_object)

        data = None
        for member in pool['server_pool_members']:
            if member['id'] == id_object:
                data = DataSpec().pool_comp_unit(member, pool['id'])
        return data
