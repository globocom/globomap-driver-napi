import mock
import unittest2
from mock import MagicMock
from mock import Mock
from mock import patch

from globomap_driver_napi.driver import Napi
from globomap_driver_napi.driver import NetworkAPI
from tests.util import open_json


class TestDriver(unittest2.TestCase):

    maxDiff = None

    def tearDown(self):
        patch.stopall()

    def _mock(self):
        # Mock connection with queue
        patch('globomap_driver_napi.driver.pika.BlockingConnection').start()

    def _mock_vip(self):
        # Mock return of vip
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vip').start()
        data = open_json('tests/json/driver/vip.json')
        napi_mock.return_value = data['vips'][0]

    def _mock_pool_member_id(self):
        # Mock return of pool_comp_unit
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_pool_by_member_id').start()
        data = open_json('tests/json/driver/pool.json')
        napi_mock.return_value = data['server_pools'][0]

    def test_driver_vip(self):
        self._mock()
        self._mock_vip()

        napi = Napi()
        data = napi.vip(1)

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

    def test_driver_pool(self):
        self._mock()

        # Mock return of pool
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_pool').start()
        data = open_json('tests/json/driver/pool.json')
        napi_mock.return_value = data['server_pools'][0]

        napi = Napi()
        data = napi.pool(1)

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

    def test_driver_port(self):
        self._mock()

        # Mock return of port
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vip_by_portpool_id').start()
        data = open_json('tests/json/driver/vip.json')
        napi_mock.return_value = data['vips'][0]

        napi = Napi()
        data = napi.port(1)

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

    def test_driver_pool_comp_unit(self):
        self._mock()
        self._mock_pool_member_id()

        napi = Napi()
        data = napi.pool_comp_unit(1)

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
        self._mock()
        self._mock_pool_member_id()

        napi = Napi()
        data = napi.comp_unit(1)

        expected = {
            'content': {
                'id': u'SERVERSPACE1',
                'name': u'SERVERSPACE1'
            },
            'collection': 'comp_unit'
        }

        self.assertDictEqual(data, expected)

    def test_map(self):
        self._mock()

        keys = Napi()._map().keys()
        expected = ['VipRequest', 'VipRequestPortPool',
                    'ServerPool', 'ServerPoolMember']

        self.assertListEqual(sorted(keys), sorted(expected))

    def test_get_msg_create(self):
        self._mock()
        self._mock_vip()

        napi = Napi()
        vip_key = napi._map().get('VipRequest')[0]
        message = {
            'action': 'Cadastrar',
            'kind': 'VipRequest',
            'data': {
                'new_value': 'whatever',
                'old_value': 'whatever',
                'user': 1,
                'id_object': 1
            },
            'timestamp': 1501264297
        }
        data = napi._get_msg(vip_key, message)

        expected = {
            'action': 'CREATE',
            'element': {
                'content': {
                    'properties': {
                        'ip': u'10.16.0.2',
                        'environmentvip': 'FIN_VIP-ClientTxt-VIP-EnvP44Txt-VIP',
                        'created': False
                    },
                    'id': 1,
                    'name': u'vip_teste',
                    'provider': 'napi',
                    'timestamp': 1501264297
                },
                'collection': 'vip'
            }
        }
        self.assertDictEqual(data, expected)

    def test_get_msg_update(self):
        self._mock()
        self._mock_vip()

        napi = Napi()
        vip_key = napi._map().get('VipRequest')[0]
        message = {
            'action': 'Alterar',
            'kind': 'VipRequest',
            'data': {
                'new_value': 'whatever',
                'old_value': 'whatever',
                'user': 1,
                'id_object': 1
            },
            'timestamp': 1501264297
        }
        data = napi._get_msg(vip_key, message)

        expected = {
            'action': 'UPDATE',
            'element': {
                'content': {
                    'properties': {
                        'ip': u'10.16.0.2',
                        'environmentvip': 'FIN_VIP-ClientTxt-VIP-EnvP44Txt-VIP',
                        'created': False
                    },
                    'id': 1,
                    'name': u'vip_teste',
                    'provider': 'napi',
                    'timestamp': 1501264297
                },
                'collection': 'vip'
            }
        }
        self.assertDictEqual(data, expected)

    def test_get_msg_delete(self):
        self._mock()

        napi = Napi()
        vip_key = napi._map().get('VipRequest')[0]
        message = {
            'action': 'Remover',
            'kind': 'VipRequest',
            'data': {
                'new_value': 'whatever',
                'old_value': 'whatever',
                'user': 1,
                'id_object': 1
            },
            'timestamp': 1501264297
        }
        data = napi._get_msg(vip_key, message)

        expected = {
            'action': 'DELETE',
            'element': {
                'content': {
                    'id': 1,
                    'provider': 'napi'
                },
                'collection': 'vip'
            }
        }
        self.assertDictEqual(data, expected)

    def mock_updates(self):
        self._mock()
        self._mock_vip()
        self._mock_pool_member_id()

        napi_mock = patch(
            'globomap_driver_napi.driver.Napi._consumer').start()

        data = open_json('tests/json/messages.json')
        napi = Napi()
        napi._consumer.return_value = iter(data)

        return napi

    def test_get_messages(self):
        napi = self.mock_updates()

        data = open_json('tests/json/return_messages.json')

        for i in range(3):
            msg = napi._get_messages()
            self.assertDictEqual(msg[0], data[i])

        msg = napi._get_messages()
        self.assertDictEqual(msg[0], data[3])
        self.assertDictEqual(msg[1], data[4])

        with self.assertRaises(StopIteration):
            msg = napi._get_messages()

    def teste_updates(self):
        napi = self.mock_updates()

        data = open_json('tests/json/return_messages.json')

        for i in range(5):
            msg = napi.updates()
            self.assertDictEqual(msg[0], data[i])

        with self.assertRaises(StopIteration):
            msg = napi.updates()

        with self.assertRaises(StopIteration):
            msg = napi.updates()


if __name__ == '__main__':
    unittest2.main()
