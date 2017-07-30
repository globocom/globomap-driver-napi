import mock
import unittest2
from mock import MagicMock
from mock import Mock
from mock import patch

from globomap_driver_napi.driver import Napi
from globomap_driver_napi.driver import NetworkAPI
from globomap_driver_napi.settings import MAP_FUNC
from tests.util import open_json


class TestDriver(unittest2.TestCase):

    maxDiff = None

    def tearDown(self):
        patch.stopall()

    def test_vip_treat_message_create(self):
        self._mock_pika()
        self._mock_vip()

        napi = Napi()
        kind = MAP_FUNC.get('VipRequest')[0]
        message = self._make_message('Cadastrar', 'VipRequest')
        data = napi._treat_message(kind, message)

        self._assert_vip('CREATE', data)

    def test_vip_treat_message_update(self):
        self._mock_pika()
        self._mock_vip()

        napi = Napi()
        kind = MAP_FUNC.get('VipRequest')[0]
        message = self._make_message('Alterar', 'VipRequest')
        data = napi._treat_message(kind, message)

        self._assert_vip('UPDATE', data)

    def test_vip_treat_message_delete(self):
        self._mock_pika()

        napi = Napi()
        kind = MAP_FUNC.get('VipRequest')[0]
        message = self._make_message('Remover', 'VipRequest')
        data = napi._treat_message(kind, message)

        self._asset_msg_delete('napi', 'vip', data)

    def test_port_treat_message_create(self):
        self._mock_pika()
        self._mock_vip_by_portpool_id()

        napi = Napi()
        kind = MAP_FUNC.get('VipRequestPortPool')[0]
        message = self._make_message('Cadastrar', 'VipRequestPortPool')
        data = napi._treat_message(kind, message)

        self._assert_port('CREATE', data)

    def test_port_treat_message_update(self):
        self._mock_pika()
        self._mock_vip_by_portpool_id()

        napi = Napi()
        kind = MAP_FUNC.get('VipRequestPortPool')[0]
        message = self._make_message('Alterar', 'VipRequestPortPool')
        data = napi._treat_message(kind, message)

        self._assert_port('UPDATE', data)

    def test_port_treat_message_delete(self):
        self._mock_pika()

        napi = Napi()
        kind = MAP_FUNC.get('VipRequestPortPool')[0]
        message = self._make_message('Remover', 'VipRequestPortPool')
        data = napi._treat_message(kind, message)

        self._asset_msg_delete('napi', 'port', data)

    def test_pool_treat_message_create(self):
        self._mock_pika()
        self._mock_pool()

        napi = Napi()
        kind = MAP_FUNC.get('ServerPool')[0]
        message = self._make_message('Cadastrar', 'ServerPool')
        data = napi._treat_message(kind, message)

        self._assert_pool('CREATE', data)

    def test_pool_treat_message_update(self):
        self._mock_pika()
        self._mock_pool()

        napi = Napi()
        kind = MAP_FUNC.get('ServerPool')[0]
        message = self._make_message('Alterar', 'ServerPool')
        data = napi._treat_message(kind, message)

        self._assert_pool('UPDATE', data)

    def test_pool_treat_message_delete(self):
        self._mock_pika()

        napi = Napi()
        kind = MAP_FUNC.get('ServerPool')[0]
        message = self._make_message('Remover', 'ServerPool')
        data = napi._treat_message(kind, message)

        self._asset_msg_delete('napi', 'pool', data)

    def test_pool_comp_unit_treat_message_create(self):
        self._mock_pika()
        self._mock_pool_member_id()

        napi = Napi()
        kind = MAP_FUNC.get('ServerPoolMember')[0]
        message = self._make_message('Cadastrar', 'ServerPoolMember')
        data = napi._treat_message(kind, message)

        self._assert_pool_comp_unit('CREATE', data)

    def test_pool_comp_unit_treat_message_update(self):
        self._mock_pika()
        self._mock_pool_member_id()

        napi = Napi()
        kind = MAP_FUNC.get('ServerPoolMember')[0]
        message = self._make_message('Alterar', 'ServerPoolMember')
        data = napi._treat_message(kind, message)

        self._assert_pool_comp_unit('UPDATE', data)

    def test_pool_comp_unit_treat_message_delete(self):
        self._mock_pika()

        napi = Napi()
        kind = MAP_FUNC.get('ServerPoolMember')[0]
        message = self._make_message('Remover', 'ServerPoolMember')
        data = napi._treat_message(kind, message)

        self._asset_msg_delete('napi', 'pool_comp_unit', data)

    def test_comp_unit_treat_message_create(self):
        self._mock_pika()
        self._mock_pool_member_id()

        napi = Napi()
        kind = MAP_FUNC.get('ServerPoolMember')[1]
        message = self._make_message('Cadastrar', 'ServerPoolMember')
        data = napi._treat_message(kind, message)

        self._assert_comp_unit('CREATE', data)

    def test_comp_unit_treat_message_update(self):
        self._mock_pika()
        self._mock_pool_member_id()

        napi = Napi()
        kind = MAP_FUNC.get('ServerPoolMember')[1]
        message = self._make_message('Alterar', 'ServerPoolMember')
        data = napi._treat_message(kind, message)

        self._assert_comp_unit('UPDATE', data)

    def test_comp_unit_treat_message_delete(self):
        self._mock_pika()

        napi = Napi()
        kind = MAP_FUNC.get('ServerPoolMember')[1]
        message = self._make_message('Remover', 'ServerPoolMember')
        data = napi._treat_message(kind, message)

        self._asset_msg_delete('globomap', 'comp_unit', data)

    #########
    # MOCKS #
    #########
    def _mock_pika(self):
        patch('globomap_driver_napi.driver.pika.BlockingConnection').start()

    def _mock_vip(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vip').start()
        data = open_json('tests/json/driver/vip.json')
        napi_mock.return_value = data['vips'][0]

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

    def _mock_pool_member_id(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_pool_by_member_id').start()
        data = open_json('tests/json/driver/pool.json')
        napi_mock.return_value = data['server_pools'][0]

    def _assert_vip(self, action, data):
        expected = {
            'action': action,
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

    def _assert_port(self, action, data):
        expected = {
            'action': action,
            'element': {
                'content': {
                    'id': 1,
                    'name': '8080',
                    'provider': 'napi',
                    'timestamp': 1501264297
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
        }

        self.assertDictEqual(data, expected)

    def _assert_pool(self, action, data):
        expected = {
            'action': action,
            'element': {
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
                    'name': u'Pool_1',
                    'timestamp': 1501264297,
                    'provider': 'napi'
                },
                'collection': 'pool'
            }
        }

        self.assertDictEqual(data, expected)

    def _assert_pool_comp_unit(self, action, data):
        expected = {
            'action': action,
            'element': {
                'content': {
                    'properties': {
                        'priority': 0,
                        'ip': u'10.0.0.2',
                        'limit': 1000,
                        'weight': 1,
                        'port_real': 8080
                    },
                    'id': 1,
                    'name': u'10.0.0.2',
                    'timestamp': 1501264297,
                    'provider': 'napi'
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
        }

        self.assertDictEqual(data, expected)

    def _assert_comp_unit(self, action, data):
        expected = {
            'action': action,
            'element': {
                'content': {
                    'id': u'SERVERSPACE1',
                    'name': u'SERVERSPACE1',
                    'timestamp': 1501264297,
                    'provider': 'globomap'
                },
                'collection': 'comp_unit'
            }
        }

        self.assertDictEqual(data, expected)

    def _asset_msg_delete(self, provider, collection, data):
        expected = {
            'action': 'DELETE',
            'element': {
                'content': {
                    'id': 1,
                    'provider': provider
                },
                'collection': collection
            }
        }
        self.assertDictEqual(data, expected)

    def _make_message(self, action, kind):
        message = {
            'action': action,
            'kind': kind,
            'data': {
                'new_value': 'whatever',
                'old_value': 'whatever',
                'user': 1,
                'id_object': 1
            },
            'timestamp': 1501264297
        }

        return message


if __name__ == '__main__':
    unittest2.main()
