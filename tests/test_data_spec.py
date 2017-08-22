import json

import mock
import unittest2

from globomap_driver_napi.data_spec import DataSpec
from tests.util import open_json


class TestDataSpec(unittest2.TestCase):

    maxDiff = None

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
        """Test method vip of DataSpec"""

        vip = open_json('tests/json/data_spec/vip.json')
        data = DataSpec().vip(vip)
        expected = {
            'id': '1',
            'name': 'vip_teste',
            'provider': 'napi',
            'properties': [
                {
                    'key': 'created',
                    'value': False,
                    'description': 'Created id Load Balancer'
                },
                {
                    'key': 'ip',
                    'value': '10.10.0.2',
                    'description': 'IP'
                },
                {
                    'key': 'environmentvip',
                    'value': 'FIN_VIP-ClientTxt-VIP-EnvP44Txt-VIP',
                    'description': 'Environment of VIP'
                }
            ]
        }

        self.assertDictEqual(data, expected)

    def test_data_spec_port(self):
        """Test method port of DataSpec"""

        vip = open_json('tests/json/data_spec/port.json')
        data = DataSpec().port(vip, 1)
        expected = {
            'from': 'vip/napi_1',
            'to': 'pool/napi_1',
            'id': '1',
            'name': '8080',
            'provider': 'napi'
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_pool(self):
        """Test method pool of DataSpec"""

        pool = open_json('tests/json/data_spec/pool.json')
        data = DataSpec().pool(pool)
        expected = {
            'id': '1',
            'name': 'Pool_1',
            'provider': 'napi',
            'properties': [
                {
                    'key': 'default_port',
                    'value': 8080,
                    'description': 'Default Port of Pool'
                },
                {
                    'key': 'environment',
                    'value': 'DIVISAO_DC_POOL - AMBIENTE_LOGICO_POOL - GRUPO_L3_POOL',
                    'description': 'Environment of Pool'
                },
                {
                    'key': 'servicedownaction',
                    'value': 'none',
                    'description': 'Action On Service Down'
                },
                {
                    'key': 'healthcheck',
                    'value': 'TCP',
                    'description': 'Healthcheck Type'
                },
                {
                    'key': 'lb_method',
                    'value': 'least-conn',
                    'description': 'Method of Load Balancing'
                },
                {
                    'key': 'default_limit',
                    'value': 100,
                    'description': 'Limit of Connections'
                },
                {
                    'key': 'pool_created',
                    'value': True,
                    'description': 'Created in Load Balancer'
                }
            ]
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_pool_comp_unit(self):
        """Test method pool_comp_unit of DataSpec"""

        pool_comp_unit = open_json('tests/json/data_spec/pool_comp_unit.json')
        data = DataSpec().pool_comp_unit(pool_comp_unit, 1)
        expected = {
            'from': 'pool/napi_1',
            'to': 'comp_unit/globomap_serverspace1',
            'id': '1',
            'name': '10.0.0.2',
            'provider': 'napi',
            'properties': [
                {
                    'key': 'ip',
                    'value': u'10.0.0.2',
                    'description': 'IP'
                },
                {
                    'key': 'priority',
                    'value': 0,
                    'description': 'Priority'
                },
                {
                    'key': 'weight',
                    'value': 1,
                    'description': 'Weight'
                },
                {
                    'key': 'limit',
                    'value': 1000,
                    'description': 'Limit'
                },
                {
                    'key': 'port_real',
                    'value': 8080,
                    'description': 'Port'
                }
            ]
        }

        self.assertDictEqual(data, expected)

    def test_data_spec_comp_unit(self):
        """Test method comp_unit of DataSpec"""

        comp_unit = open_json('tests/json/data_spec/comp_unit.json')
        data = DataSpec().comp_unit(comp_unit)
        expected = {
            'id': 'eqpt1',
            'name': '',
            'provider': 'globomap',
            'properties': [
                {
                    'key': 'maintenance',
                    'value': False,
                    'description': 'Maintenance'
                },
                {
                    'key': 'equipment_type',
                    'value': 'Server',
                    'description': 'Equipment Type'
                },
                {
                    'key': 'ips',
                    'value': [
                        '10.0.0.1',
                        'bebe:bebe:bebe:0000:0000:0000:0000:0001'
                    ],
                    'description': 'IPs'
                },
            ]
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_network_v4_comp_unit(self):
        """Test method network_comp_unit(v4) of DataSpec"""

        network = open_json('tests/json/data_spec/network_v4_comp_unit.json')
        data = DataSpec().network_comp_unit(network, 'EQPT1', 8)
        expected = {
            'from': 'network/napi_v4_3',
            'to': 'comp_unit/globomap_eqpt1',
            'id': 'v4_8',
            'name': '10.0.0.5 - eqpt1',
            'provider': 'napi',
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_network_v6_comp_unit(self):
        """Test method network_comp_unit(v6) of DataSpec"""

        network = open_json('tests/json/data_spec/network_v6_comp_unit.json')
        data = DataSpec().network_comp_unit(network, 'EQPT1', 6)
        expected = {
            'from': 'network/napi_v6_2',
            'to': 'comp_unit/globomap_eqpt1',
            'id': 'v6_6',
            'name': 'fdbe:bebe:bebe:bebe:0000:0000:0000:0001 - eqpt1',
            'provider': 'napi',
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_network_v4(self):
        """Test method network(v4) of DataSpec"""

        network = open_json('tests/json/data_spec/network_v4.json')
        data = DataSpec().network(network)
        expected = {
            'id': 'v4_1',
            'name': '10.0.0.0/24',
            'provider': 'napi',
            'properties': [
                {
                    'key': 'active',
                    'value': True,
                    'description': 'Network Status'
                },
                {
                    'key': 'network_type',
                    'value': 'Point-to-Point',
                    'description': 'Network Type'
                }
            ]
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_network_v6(self):
        """Test method network(v6) of DataSpec"""

        network = open_json('tests/json/data_spec/network_v6.json')
        data = DataSpec().network(network)
        expected = {
            'id': 'v6_1',
            'name': 'bebe:bebe:bebe:0000:0000:0000:0000:0000/64',
            'provider': 'napi',
            'properties': [
                {
                    'key': 'active',
                    'value': False,
                    'description': 'Network Status'
                },
                {
                    'key': 'network_type',
                    'value': 'Point-to-Point',
                    'description': 'Network Type'
                }
            ]
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_vlan_network_v4(self):
        """Test method vlan_network(v4) of DataSpec"""

        network = open_json('tests/json/data_spec/network_v4.json')
        data = DataSpec().vlan_network(network)
        expected = {
            'from': 'vlan/napi_3',
            'to': 'network/napi_v4_1',
            'id': 'v4_1',
            'name': '31 - 10.0.0.0/24',
            'provider': 'napi',
        }
        self.assertDictEqual(data, expected)
        self.assertDictEqual(data, expected)

    def test_data_spec_vlan_network_v6(self):
        """Test method vlan_network(v6) of DataSpec"""

        network = open_json('tests/json/data_spec/network_v6.json')
        data = DataSpec().vlan_network(network)
        expected = {
            'from': 'vlan/napi_3',
            'to': 'network/napi_v6_1',
            'id': 'v6_1',
            'name': '31 - bebe:bebe:bebe:0000:0000:0000:0000:0000/64',
            'provider': 'napi',
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_vlan(self):
        """Test method vlan of DataSpec"""

        vlan = open_json('tests/json/data_spec/vlan.json')
        data = DataSpec().vlan(vlan)
        expected = {
            'id': '1',
            'name': 'Vlan1',
            'provider': 'napi',
            'properties': [
                {
                    'key': 'num_vlan',
                    'value': 2,
                    'description': 'Number of VLAN'
                },
                {
                    'key': 'description',
                    'value': 'Vlan Description',
                    'description': 'Description'
                },
                {
                    'value': False,
                    'key': 'active',
                    'description': 'Status'
                }
            ]
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_environment_vlan(self):
        """Test method environment_vlan of DataSpec"""

        vlan = open_json('tests/json/data_spec/vlan.json')
        data = DataSpec().environment_vlan(vlan)
        name = 'DIVISAO_DC_SPACE_2 - AMBIENTE_LOGICO_SPACE_2 - ' \
            'GRUPO_L3_SPACE_2 / 2'

        expected = {
            'from': 'environment/napi_3',
            'to': 'vlan/napi_1',
            'id': '1',
            'name': name,
            'provider': 'napi',
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_environment(self):
        """Test method environment of DataSpec"""

        environment = open_json('tests/json/data_spec/environment.json')
        data = DataSpec().environment(environment)
        expected = {
            'id': '1',
            'name': 'DIVISAO_DC_SPACE_2 - AMBIENTE_LOGICO_SPACE_2 - GRUPO_L3_SPACE_2',
            'provider': 'napi',
            'properties': [
                {
                    'key': 'default_vrf',
                    'value': 'default',
                    'description': 'Default VRF'
                }
            ]
        }
        self.assertDictEqual(data, expected)

    def test_data_spec_father_environment(self):
        """Test method father_environment of DataSpec"""

        environment = open_json('tests/json/data_spec/environment.json')
        data = DataSpec().father_environment(environment)
        name = 'DIVISAO_DC_SPACE_2 - AMBIENTE_LOGICO_SPACE_2 - GRUPO_L3_SPACE_2 / ' \
            'DIVISAO_DC_YELLOW - AMBIENTE_LOGICO_YELLOW - GRUPO_L3_YELLOW'
        expected = {
            'from': 'environment/napi_7',
            'to': 'environment/napi_1',
            'id': '1',
            'name': name,
            'provider': 'napi'
        }
        self.assertDictEqual(data, expected)


if __name__ == '__main__':
    unittest2.main()
