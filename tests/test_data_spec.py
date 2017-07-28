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
        vip = open_json('tests/json/vip.json')
        data = DataSpec().vip(vip)
        expected = {
            'collection': 'vip',
            'content': {
                'id': 1,
                'name': 'vip_teste',
                'properties': {
                    'ip': '10.10.0.2',
                    'created': False,
                    'environmentvip': 'FIN_VIP-ClientTxt-VIP-EnvP44Txt-VIP'
                }
            }
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_port(self):
        vip = open_json('tests/json/port.json')
        data = DataSpec().port(vip, 1)
        expected = {
            'collection': 'port',
            'from': {
                'collection': 'vip',
                'provider': 'napi',
                'id': 1
            },
            'to': {
                'collection': 'pool',
                'provider': 'napi',
                'id': 1
            },
            'content': {
                'id': 1,
                'name': '8080'
            }
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_pool(self):
        pool = open_json('tests/json/pool.json')
        data = DataSpec().pool(pool)
        expected = {
            'collection': 'pool',
            'content': {
                'id': 1,
                'name': 'Pool_1',
                'properties': {
                    'default_port': 8080,
                    'environment': 'DIVISAO_DC_POOL - ' +
                                   'AMBIENTE_LOGICO_POOL - GRUPO_L3_POOL',
                    'servicedownaction': 'none',
                    'healthcheck': 'TCP',
                    'lb_method': 'least-conn',
                    'default_limit': 100,
                    'pool_created': True
                }
            }
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_pool_comp_unit(self):
        vip = open_json('tests/json/pool_comp_unit.json')
        data = DataSpec().pool_comp_unit(vip, 1)
        expected = {
            'collection': 'pool_comp_unit',
            'from': {
                'collection': 'pool',
                'provider': 'napi',
                'id': 1
            },
            'to': {
                'collection': 'comp_unit',
                'provider': 'globomap',
                'id': 'SERVERSPACE1'
            },
            'content': {
                'id': 1,
                'name': '10.0.0.2',
                'properties': {
                    'priority': 0,
                    'ip': u'10.0.0.2',
                    'limit': 1000,
                    'weight': 1,
                    'port_real': 8080
                }
            }
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_comp_unit(self):
        pool = open_json('tests/json/comp_unit.json')
        data = DataSpec().comp_unit(pool)
        expected = {
            'collection': 'comp_unit',
            'content': {
                'id': 'SERVERSPACE1',
                'name': 'SERVERSPACE1'
            }
        }
        self.assertDictEqual(data, expected)


if __name__ == '__main__':
    unittest2.main()
