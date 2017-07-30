import unittest2
from mock import patch

from globomap_driver_napi.kind import Kind
from tests.util import open_json


class TestKind(unittest2.TestCase):

    maxDiff = None

    def tearDown(self):
        patch.stopall()

    def test_driver_vip(self):
        self._mock_vip()

        kind = Kind()
        data = kind.vip(1)

        expected = {
            'content': {
                'properties': {
                    'ip': u'10.16.0.2',
                    'environmentvip':
                    'FIN_VIP-ClientTxt-VIP-EnvP44Txt-VIP',
                    'created': False
                },
                'id': 1,
                'name': u'vip_teste'
            },
            'collection': 'vip'
        }
        self.assertDictEqual(data, expected)

    def test_driver_port(self):
        self._mock_vip_by_portpool_id()

        kind = Kind()
        data = kind.port(1)

        expected = {
            'content': {
                'id': 1,
                'name': '8080'
            },
            'to': {
                'id': 1,
                'collection': 'pool',
                'provider': 'napi'
            },
            'from': {
                'id': 1,
                'collection': 'vip',
                'provider': 'napi'
            },
            'collection': 'port'
        }
        self.assertDictEqual(data, expected)

    def test_driver_pool(self):
        self._mock_pool()

        kind = Kind()
        data = kind.pool(1)

        expected = {
            'content': {
                'properties': {
                    'lb_method': u'least-conn',
                    'healthcheck': u'TCP',
                    'pool_created': True,
                    'environment': u'DIVISAO_DC_POOL - ' +
                    'AMBIENTE_LOGICO_POOL - GRUPO_L3_POOL',
                    'servicedownaction': u'none',
                    'default_port': 8080,
                    'default_limit': 100
                },
                'id': 1,
                'name': u'Pool_1'
            },
            'collection': 'pool'
        }
        self.assertDictEqual(data, expected)

    def test_driver_pool_comp_unit(self):
        self._mock_pool_member_id()

        kind = Kind()
        data = kind.pool_comp_unit(1)

        expected = {
            'content': {
                'properties': {
                    'priority': 0,
                    'ip': u'10.0.0.2',
                    'limit': 1000,
                    'weight': 1,
                    'port_real': 8080
                },
                'id': 1,
                'name': u'10.0.0.2'
            },
            'to': {
                'id': u'SERVERSPACE1',
                'collection': 'comp_unit',
                'provider': 'globomap'
            },
            'from': {
                'id': 1,
                'collection':
                'pool',
                'provider': 'napi'
            },
            'collection': 'pool_comp_unit'
        }
        self.assertDictEqual(data, expected)

    def test_driver_comp_unit(self):
        self._mock_pool_member_id()

        kind = Kind()
        data = kind.comp_unit(1)

        expected = {
            'content': {
                'id': u'SERVERSPACE1',
                'name': u'SERVERSPACE1'
            },
            'collection': 'comp_unit'
        }

        self.assertDictEqual(data, expected)

    def _mock_vip(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vip').start()
        data = open_json('tests/json/driver/vip.json')
        napi_mock.return_value = data['vips'][0]

    def _mock_pool_member_id(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_pool_by_member_id').start()
        data = open_json('tests/json/driver/pool.json')
        napi_mock.return_value = data['server_pools'][0]

    def _mock_vip_by_portpool_id(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vip_by_portpool_id').start()
        data = open_json('tests/json/driver/vip.json')
        napi_mock.return_value = data['vips'][0]

    def _mock_pool(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_pool').start()
        data = open_json('tests/json/driver/pool.json')
        napi_mock.return_value = data['server_pools'][0]


if __name__ == '__main__':
    unittest2.main()
