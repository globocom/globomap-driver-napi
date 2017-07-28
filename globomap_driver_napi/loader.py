from .data_spec import DataSpec
from .networkapi import NetworkAPI


class Loader(object):

    def __init__(self):
        self.search = {'asorting_cols': ['-id']}
        self.client = NetworkAPI().client

    def vips(self):

        obj = self.client.create_api_vip_request()
        for vips in self._paging(obj, 'vips', self.search):
            for vip in vips:
                data = DataSpec().vip(vip)

    def pools(self):
        """Load pools"""

        obj = self.client.create_api_pool()
        for pools in self._paging(obj, 'server_pools', self.search):
            for pool in pools:
                data = DataSpec().pool(pool)

    def _paging(self, obj, key, next_search):

        while True:
            objs = obj.search(search=next_search)
            if objs[key]:
                next_search = objs['next_search']
                yield objs[key]
            else:
                break
