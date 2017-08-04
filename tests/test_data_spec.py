import json

import mock
import unittest2

from globomap_driver_napi.data_spec import DataSpec
from tests.util import open_json


class TestDataSpec(unittest2.TestCase):

    def test_data_spec_vip_with_list(self):
        with self.assertRaises(Exception):
            DataSpec().vip(list())

    def test_data_spec_port_with_list(self):
        with self.assertRaises(Exception):
            DataSpec().port(list(), 1)

    def test_data_spec_pool_with_list(self):
        with self.assertRaises(Exception):
            DataSpec().pool(list())

    def test_data_spec_pool_comp_unit_with_list(self):
        with self.assertRaises(Exception):
            DataSpec().pool_comp_unit(list(), 1)

    def test_data_spec_comp_unit_with_list(self):
        with self.assertRaises(Exception):
            DataSpec().comp_unit(list())

    def test_data_spec_vip(self):
        vip = open_json('tests/json/data_spec/vip.json')
        data = DataSpec().vip(vip)
        expected = {
            'id': 1,
            'name': 'vip_teste',
            'provider': 'napi',
            'properties': [
                {'key': 'created', 'value': False},
                {'key': 'ip', 'value': '10.10.0.2'},
                {'key': 'environmentvip', 'value': 'FIN_VIP-ClientTxt-VIP-EnvP44Txt-VIP'}
            ]
        }

        self.assertDictEqual(data, expected)

    def test_data_spec_port(self):
        vip = open_json('tests/json/data_spec/port.json')
        data = DataSpec().port(vip, 1)
        expected = {
            'from': 'vip/napi_1',
            'to': 'pool/napi_1',
            'id': 1,
            'name': '8080',
            'provider': 'napi'
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_pool(self):
        pool = open_json('tests/json/data_spec/pool.json')
        data = DataSpec().pool(pool)
        expected = {
            'id': 1,
            'name': 'Pool_1',
            'provider': 'napi',
            'properties': [
                {
                    'key': 'default_port',
                    'value': 8080
                },
                {
                    'key': 'environment',
                    'value': 'DIVISAO_DC_POOL - ' +
                             'AMBIENTE_LOGICO_POOL - GRUPO_L3_POOL'
                },
                {
                    'key': 'servicedownaction',
                    'value': 'none'
                },
                {
                    'key': 'healthcheck',
                    'value': 'TCP'
                },
                {
                    'key': 'lb_method',
                    'value': 'least-conn'
                },
                {
                    'key': 'default_limit',
                    'value': 100
                },
                {
                    'key': 'pool_created',
                    'value': True
                }
            ]
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_pool_comp_unit(self):
        vip = open_json('tests/json/data_spec/pool_comp_unit.json')
        data = DataSpec().pool_comp_unit(vip, 1)
        expected = {
            'from': 'pool/napi_1',
            'to': 'comp_unit/globomap_SERVERSPACE1',
            'id': 1,
            'name': '10.0.0.2',
            'provider': 'napi',
            'properties': [
                {'key': 'ip', 'value': u'10.0.0.2'},
                {'key': 'priority', 'value': 0},
                {'key': 'weight', 'value': 1},
                {'key': 'limit', 'value': 1000},
                {'key': 'port_real', 'value': 8080}
            ]
        }

        self.assertDictEqual(data, expected)

    def test_data_spec_comp_unit(self):
        pool = open_json('tests/json/data_spec/comp_unit.json')
        data = DataSpec().comp_unit(pool)
        expected = {
            'id': 'SERVERSPACE1',
            'name': 'SERVERSPACE1',
            'provider': 'globomap'
        }
        self.assertDictEqual(data, expected)


if __name__ == '__main__':
    unittest2.main()
