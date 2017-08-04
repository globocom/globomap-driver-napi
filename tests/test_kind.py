import unittest2
from mock import patch

from globomap_driver_napi.kind import Kind
from tests.util import open_json


class TestKind(unittest2.TestCase):

    maxDiff = None

    def tearDown(self):
        patch.stopall()

    def _open_message(self):
        data = open_json('tests/json/queue_messages.json')
        return data

    def _open_return_message(self):
        data = open_json('tests/json/update_messages.json')
        return data

    def test_vip(self):
        self._mock_vip()

        data = self._open_message()[0:3]
        data_ret = self._open_return_message()[0:3]

        for i in range(3):
            kind = Kind()
            res = kind.vip(data[i])
            self.assertDictEqual(res, data_ret[i])

    def test_port(self):
        self._mock_vip_by_portpool_id()

        data = self._open_message()[3:6]
        data_ret = self._open_return_message()[3:6]

        for i in range(3):
            kind = Kind()
            res = kind.port(data[i])
            self.assertDictEqual(res, data_ret[i])

    def test_pool(self):
        self._mock_pool()

        data = self._open_message()[6:9]
        data_ret = self._open_return_message()[6:9]

        for i in range(3):
            kind = Kind()
            res = kind.pool(data[i])
            self.assertDictEqual(res, data_ret[i])

    def test_driver_pool_comp_unit(self):
        self._mock_pool_member_id()

        data = self._open_message()[9:12]
        data_ret = self._open_return_message()[9:12]

        for i in range(3):
            kind = Kind()
            res = kind.pool_comp_unit(data[i])
            self.assertDictEqual(res, data_ret[i])

    def _mock_vip(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vip').start()
        data = open_json('tests/json/driver/get_vip.json')
        napi_mock.return_value = data['vips'][0]

    def _mock_pool_member_id(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_pool_by_member_id').start()
        data = open_json('tests/json/driver/get_pool.json')
        napi_mock.return_value = data['server_pools'][0]

    def _mock_vip_by_portpool_id(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vip_by_portpool_id').start()
        data = open_json('tests/json/driver/get_vip.json')
        napi_mock.return_value = data['vips'][0]

    def _mock_pool(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_pool').start()
        data = open_json('tests/json/driver/get_pool.json')
        napi_mock.return_value = data['server_pools'][0]


if __name__ == '__main__':
    unittest2.main()
