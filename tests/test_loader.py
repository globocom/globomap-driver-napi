from copy import deepcopy

import unittest2
from mock import patch
from util import open_json

from globomap_driver_napi.loader import Loader


class TestLoader(unittest2.TestCase):

    maxDiff = None

    def setUp(self):
        time_mock = patch('globomap_driver_napi.loader.time').start()
        time_mock.return_value = 1501448160

    def test_vip_2_pages(self):
        requests_mock = self._mock_vip()

        data = open_json('tests/json/driver/get_vip.json')
        data_ret = open_json('tests/json/loader/return_vips.json')

        vips = self._search()
        data.update(vips)

        vip2 = deepcopy(data['vips'][0])
        data['vips'].append(vip2)

        data2 = deepcopy(data_ret)
        data_ret += (data2)

        requests_mock.return_value = data

        # First Page
        self._page_vip(vips, data_ret)
        # Second Page
        self._page_vip(vips, data_ret)

    def test_pool_2_pages(self):
        requests_mock = self._mock_pool()

        data = open_json('tests/json/driver/get_pool.json')
        data_ret = open_json('tests/json/loader/return_pools.json')

        pools = self._search()
        data.update(pools)

        pool2 = deepcopy(data['server_pools'][0])
        data['server_pools'].append(pool2)

        data2 = deepcopy(data_ret)
        data_ret += (data2)

        requests_mock.return_value = data

        # First Page
        self._page_pool(pools, data_ret)
        # Second Page
        self._page_pool(pools, data_ret)

    def test_pool_page_stop(self):
        requests_mock = self._mock_pool()

        data = {'server_pools': []}
        requests_mock.return_value = data
        with self.assertRaises(StopIteration):
            Loader().pools().next()
        return requests_mock

    def test_vip_page_stop(self):
        requests_mock = self._mock_vip()

        data = {'vips': []}
        requests_mock.return_value = data
        with self.assertRaises(StopIteration):
            Loader().vips().next()

    def _search(self):
        content = {
            'prev_search': None,
            'total': 1,
            'next_search': {
                'extends_search': [],
                'end_record': 50,
                'start_record': 25,
                'searchable_columns': [],
                'asorting_cols': [
                    '-id'
                ],
                'custom_search': None
            }
        }

        return content

    def _page_vip(self, vips, data_ret):
        vips = Loader().vips().next()
        self.assertEqual(len(vips), len(data_ret))
        for key, _ in enumerate(vips):
            self.assertDictEqual(vips[key], data_ret[key])

    def _page_pool(self, pools, data_ret):
        pools = Loader().pools().next()
        self.assertEqual(len(pools), len(data_ret))
        for key, _ in enumerate(pools):
            self.assertDictEqual(pools[key], data_ret[key])

    def _mock_pool(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiPool.search').start()
        return requests_mock

    def _mock_vip(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiVipRequest.search').start()
        return requests_mock


if __name__ == '__main__':
    unittest2.main()
