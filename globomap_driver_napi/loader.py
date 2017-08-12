import json
import logging
from time import time

import requests

from globomap_driver_napi import settings
from globomap_driver_napi.data_spec import DataSpec
from globomap_driver_napi.networkapi import NetworkAPI


class Loader(object):

    log = logging.getLogger(__name__)

    def __init__(self):
        self.search = {'asorting_cols': ['-id']}
        self.client = NetworkAPI().client
        self.url = settings.GLOBOMAP_LOADER_ENDPOINT

    def _construct(self, provider, collection, type_coll, content):
        new_time = int(time())
        content['timestamp'] = new_time
        content['provider'] = provider
        data = {
            'action': 'CREATE',
            'collection': collection,
            'type': type_coll,
            'element': content
        }
        return data

    def send(self, data):

        response = requests.post(
            '{}/v1/updates'.format(self.url),
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            self.log.error('Message dont sent %s', data)

    def vips(self):
        """Load vips"""
        data_list = []

        obj = self.client.create_api_vip_request()
        pages = self._paging(obj, 'vips', self.search)
        while True:
            vips = pages.next()
            for vip in vips:

                content = DataSpec().vip(vip)
                data = self._construct('napi', 'vip', 'collections', content)
                data_list.append(data)

                for port in vip['ports']:
                    for pool in port['pools']:

                        pool['port'] = port['port']
                        content = DataSpec().port(pool, port['id'])
                        data = self._construct(
                            'napi', 'port', 'edges', content)
                        data_list.append(data)

            res = data_list
            data_list = []
            yield res

    def pools(self):
        """Load pools"""
        data_list = []

        obj = self.client.create_api_pool()
        pages = self._paging(obj, 'server_pools', self.search)
        while True:
            pools = pages.next()
            for pool in pools:

                content = DataSpec().pool(pool)
                data = self._construct('napi', 'pool', 'collections', content)
                data_list.append(data)

                for member in pool['server_pool_members']:

                    content = DataSpec().pool_comp_unit(member, pool['id'])
                    data = self._construct(
                        'napi', 'pool_comp_unit', 'edges', content)
                    data_list.append(data)

                    # eqpt = member['equipment']
                    # content = DataSpec().comp_unit(eqpt)
                    # data = self._construct(
                    #     'globomap', 'comp_unit', 'collections', content)
                    # data_list.append(data)

            res = data_list
            data_list = []
            yield res

    def _paging(self, obj, key, next_search):

        while True:
            objs = obj.search(search=next_search, kind='details')
            if objs[key]:
                next_search = objs['next_search']
                yield objs[key]
            else:
                break
