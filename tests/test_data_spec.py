"""
   Copyright 2017 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
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
            'properties': {
                'created': False,
                'ip': '10.10.0.2',
                'environmentvip': 'FIN_VIP-ClientTxt-VIP-EnvP44Txt-VIP'
            },
            'properties_metadata': {
                'created': {
                    'description': 'Created id Load Balancer'
                },
                'ip': {
                    'description': 'IP'
                },
                'environmentvip': {
                    'description': 'Environment of VIP'
                }
            }
        }

        self.assertDictEqual(data, expected)

    def test_data_spec_port(self):
        """Test method port of DataSpec"""

        port = open_json('tests/json/data_spec/port.json')
        data = DataSpec().port(port, 1)
        expected = {
            'from': 'vip/napi_1',
            'to': 'pool/napi_1',
            'id': '1',
            'name': '8080:Default VIP',
            'provider': 'napi',
            'properties': {
                'l4_protocol': 'TCP',
                'l7_protocol': 'HTTP',
                'l7_rule': 'Default VIP',
                'port': 8080
            },
            'properties_metadata': {
                'l4_protocol': {
                    'description': 'L4 Protocol'
                },
                'l7_protocol': {
                    'description': 'L7 Protocol'
                },
                'l7_rule': {
                    'description': 'L7 Rule'
                },
                'port': {
                    'description': 'Port'
                }
            }
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
            'properties': {
                'default_port': 8080,
                'environment': 'DIVISAO_DC_POOL - AMBIENTE_LOGICO_POOL - GRUPO_L3_POOL',
                'servicedownaction': 'none',
                'healthcheck': 'TCP',
                'lb_method': 'least-conn',
                'default_limit': 100,
                'pool_created': True
            },
            'properties_metadata': {
                'default_port': {
                    'description': 'Default Port of Pool'
                },
                'environment': {
                    'description': 'Environment of Pool'
                },
                'servicedownaction': {
                    'description': 'Action On Service Down'
                },
                'healthcheck': {
                    'description': 'Healthcheck Type'
                },
                'lb_method': {
                    'description': 'Method of Load Balancing'
                },
                'default_limit': {
                    'description': 'Limit of Connections'
                },
                'pool_created': {
                    'description': 'Created in Load Balancer'
                }
            }
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
            'properties': {
                'ip': u'10.0.0.2',
                'priority': 0,
                'weight': 1,
                'limit': 1000,
                'port_real': 8080
            },
            'properties_metadata': {
                'ip': {
                    'description': 'IP'
                },
                'priority': {
                    'description': 'Priority'
                },
                'weight': {
                    'description': 'Weight'
                },
                'limit': {
                    'description': 'Limit'
                },
                'port_real': {
                    'description': 'Port'
                }
            }
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
            'properties': {
                'maintenance': False,
                'equipment_type': 'Server',
                'ips': [
                    '10.0.0.1',
                    'bebe:bebe:bebe:0000:0000:0000:0000:0001'
                ],
            },
            'properties_metadata': {
                'maintenance': {
                    'description': 'Maintenance'
                },
                'equipment_type': {
                    'description': 'Equipment Type'
                },
                'ips': {
                    'description': 'IPs'
                },
            }
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
            'properties': {
                'active': True,
                'network_type': 'Point-to-Point'
            },
            'properties_metadata': {
                'active': {
                    'description': 'Network Status'
                },
                'network_type': {
                    'description': 'Network Type'
                }
            }
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
            'properties': {
                'active': False,
                'network_type': 'Point-to-Point'
            },
            'properties_metadata': {
                'active': {
                    'description': 'Network Status'
                },
                'network_type': {
                    'description': 'Network Type'
                }
            }
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
            'properties': {
                'num_vlan': 2,
                'description': 'Vlan Description',
                'active': False
            },
            'properties_metadata': {
                'num_vlan': {
                    'description': 'Number of VLAN'
                },
                'description': {
                    'description': 'Description'
                },
                'active': {
                    'description': 'Status'
                }
            }
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
            'properties': {
                'default_vrf': 'default'
            },
            'properties_metadata': {
                'default_vrf': {
                    'description': 'Default VRF'
                }
            }
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
