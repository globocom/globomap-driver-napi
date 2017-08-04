import mock
import unittest2
from mock import MagicMock
from mock import Mock
from mock import patch

from globomap_driver_napi.driver import Napi
from globomap_driver_napi.driver import NetworkAPI
from globomap_driver_napi.settings import MAP_FUNC
from tests.util import open_json


class TestMessage(unittest2.TestCase):

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

        self._asset_msg_delete('napi', 'vip', 'collections', data)

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

        self._asset_msg_delete('napi', 'port', 'edges', data)

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

        self._asset_msg_delete('napi', 'pool', 'collections', data)

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

        self._asset_msg_delete('napi', 'pool_comp_unit', 'edges', data)

    # def test_comp_unit_treat_message_create(self):
    #     self._mock_pika()
    #     self._mock_pool_member_id()

    #     napi = Napi()
    #     kind = MAP_FUNC.get('ServerPoolMember')[1]
    #     message = self._make_message('Cadastrar', 'ServerPoolMember')
    #     data = napi._treat_message(kind, message)

    #     self._assert_comp_unit('CREATE', data)

    # def test_comp_unit_treat_message_update(self):
    #     self._mock_pika()
    #     self._mock_pool_member_id()

    #     napi = Napi()
    #     kind = MAP_FUNC.get('ServerPoolMember')[1]
    #     message = self._make_message('Alterar', 'ServerPoolMember')
    #     data = napi._treat_message(kind, message)

    #     self._assert_comp_unit('UPDATE', data)

    # def test_comp_unit_treat_message_delete(self):
    #     self._mock_pika()

    #     napi = Napi()
    #     kind = MAP_FUNC.get('ServerPoolMember')[1]
    #     message = self._make_message('Remover', 'ServerPoolMember')
    #     data = napi._treat_message(kind, message)

        # self._asset_msg_delete('globomap', 'comp_unit', 'collections', data)

    #########
    # MOCKS #
    #########
    def _mock_pika(self):
        patch('globomap_driver_napi.driver.pika.BlockingConnection').start()

    def _mock_vip(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vip').start()
        data = open_json('tests/json/driver/get_vip.json')
        napi_mock.return_value = data['vips'][0]

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

    def _mock_pool_member_id(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_pool_by_member_id').start()
        data = open_json('tests/json/driver/get_pool.json')
        napi_mock.return_value = data['server_pools'][0]

    def _assert_vip(self, action, data):
        expected = {
            'action': action,
            'collection': 'vip',
            'type': 'collections',
            'element': {
                'properties': [
                    {'key': 'created', 'value': False},
                    {'key': 'ip', 'value': u'10.16.0.2'},
                    {
                        'key': 'environmentvip',
                        'value': 'FIN_VIP-ClientTxt-VIP-EnvP44Txt-VIP'
                    }
                ],
                'id': 1,
                'name': u'vip_teste',
                'provider': 'napi',
                'timestamp': 1501264297
            }
        }
        if action != 'CREATE':
            expected['element']['key'] = 'vip/napi_1'

        self.assertDictEqual(data, expected)

    def _assert_port(self, action, data):
        expected = {
            'action': action,
            'collection': 'port',
            'type': 'edges',
            'element': {
                'id': 1,
                'name': '8080',
                'provider': 'napi',
                'timestamp': 1501264297,
                'to': 'pool/napi_1',
                'from': 'vip/napi_1'
            }
        }
        if action != 'CREATE':
            expected['element']['key'] = 'port/napi_1'

        self.assertDictEqual(data, expected)

    def _assert_pool(self, action, data):
        expected = {
            'action': action,
            'collection': 'pool',
            'type': 'collections',
            'element': {
                'id': 1,
                'name': u'Pool_1',
                'timestamp': 1501264297,
                'provider': 'napi',
                'properties': [
                    {'key': 'default_port', 'value': 8080},
                    {
                        'key': 'environment',
                        'value': u'DIVISAO_DC_POOL - AMBIENTE_LOGICO_POOL - GRUPO_L3_POOL'
                    },
                    {'key': 'servicedownaction', 'value': u'none'},
                    {'key': 'healthcheck', 'value': u'TCP'},
                    {'key': 'lb_method', 'value': u'least-conn'},
                    {'key': 'default_limit', 'value': 100},
                    {'key': 'pool_created', 'value': True}
                ]
            }
        }
        if action != 'CREATE':
            expected['element']['key'] = 'pool/napi_1'

        self.assertDictEqual(data, expected)

    def _assert_pool_comp_unit(self, action, data):
        expected = {
            'action': action,
            'collection': 'pool_comp_unit',
            'type': 'edges',
            'element': {
                'to': 'comp_unit/globomap_SERVERSPACE1',
                'from': 'pool/napi_1',
                'id': 1,
                'name': u'10.0.0.2',
                'properties': [
                    {'key': 'ip', 'value': u'10.0.0.2'},
                    {'key': 'priority', 'value': 0},
                    {'key': 'weight', 'value': 1},
                    {'key': 'limit', 'value': 1000},
                    {'key': 'port_real', 'value': 8080}
                ],
                'timestamp': 1501264297,
                'provider': 'napi'
            }
        }
        if action != 'CREATE':
            expected['element']['key'] = 'pool_comp_unit/napi_1'

        self.assertDictEqual(data, expected)

    def _assert_comp_unit(self, action, data):
        expected = {
            'action': action,
            'collection': 'comp_unit',
            'type': 'collections',
            'element': {
                'id': u'SERVERSPACE1',
                'name': u'SERVERSPACE1',
                'timestamp': 1501264297,
                'provider': 'globomap'
            }
        }
        if action != 'CREATE':
            expected['element']['key'] = 'comp_unit/globomap_SERVERSPACE1'

        self.assertDictEqual(data, expected)

    def _asset_msg_delete(self, provider, collection, type_coll, data):

        expected = {
            'action': 'DELETE',
            'collection': collection,
            'type': type_coll,
            'element': {
                'key': '{}/{}_{}'.format(collection, provider, 1)
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
