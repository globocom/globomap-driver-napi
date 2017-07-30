from time import time

from .data_spec import DataSpec
from .networkapi import NetworkAPI


class Loader(object):

    def __init__(self):
        self.search = {'asorting_cols': ['-id']}
        self.client = NetworkAPI().client

    def _construct(self, collection, provider, content):
        new_time = int(time())
        data = {
            'action': 'CREATE',
            'element': {
                'collection': collection,
                'content': {
                    'timestamp': new_time,
                    'provider': provider
                }
            }
        }
        data['element']['content'].update(content)

    def vips(self):
        """Load vips"""

        obj = self.client.create_api_vip_request()
        for vips in self._paging(obj, 'vips', self.search):
            for vip in vips:
                content = DataSpec().vip(vip)
                self._construct('vip', 'napi', content)

                for port in vip['ports']:
                    for pool in port['pools']:
                        pool['port'] = port['port']
                        content = DataSpec().port(pool, port['id'])
                        self._construct('port', 'napi', content)

    def pools(self):
        """Load pools"""

        obj = self.client.create_api_pool()
        for pools in self._paging(obj, 'server_pools', self.search):
            for pool in pools:
                content = DataSpec().pool(pool)
                self._construct('pool', 'napi', content)

                for member in pool['server_pool_members']:

                    content = DataSpec().pool_comp_unit(member, pool['id'])
                    self._construct('pool_comp_unit', 'napi', content)

                    eqpt = member['equipment']
                    content = DataSpec().comp_unit(eqpt)
                    self._construct('comp_unit', 'globomap', content)

    def _paging(self, obj, key, next_search):

        while True:
            objs = obj.search(search=next_search)
            if objs[key]:
                next_search = objs['next_search']
                yield objs[key]
            else:
                break
