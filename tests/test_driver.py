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

    def test_vip_get_messages(self):
        self._mock_pika()
        self._mock_vip()
        data = self._open_message()[0:3]
        data_ret = self._open_return_message()[0:3]
        self._mock_consumer(data)

        napi = Napi()
        for i in range(3):
            msg = napi.next_message()
            self.assertDictEqual(msg[0], data_ret[i])

    def test_port_get_messages(self):
        self._mock_pika()
        self._mock_vip_by_portpool_id()
        data = self._open_message()[3:6]
        data_ret = self._open_return_message()[3:6]
        self._mock_consumer(data)

        napi = Napi()
        for i in range(3):
            msg = napi.next_message()
            self.assertDictEqual(msg[0], data_ret[i])

    def test_pool_get_messages(self):
        self._mock_pika()
        self._mock_pool()
        data = self._open_message()[6:9]
        data_ret = self._open_return_message()[6:9]
        self._mock_consumer(data)

        napi = Napi()
        for i in range(3):
            msg = napi.next_message()
            self.assertDictEqual(msg[0], data_ret[i])

    def test_pool_comp_unit_get_messages(self):
        self._mock_pika()
        self._mock_pool_member_id()
        data = self._open_message()[9:12]
        data_ret = self._open_return_message()[9:12]
        self._mock_consumer(data)

        napi = Napi()
        for i in range(3):
            msg = napi.next_message()
            self.assertDictEqual(msg[0], data_ret[i])

    def test_comp_unit_get_messages(self):
        self._mock_pika()
        self._mock_pool_member_id()
        data = self._open_message()[9:12]
        data_ret = self._open_return_message()[9:12]
        self._mock_consumer(data)

        napi = Napi()
        for i in range(3):
            msg = napi.next_message()
            self.assertDictEqual(msg[0], data_ret[i])

    def test_ignore_get_messages(self):
        self._mock_pika()
        self._mock_pool_member_id()
        data = self._open_message()[12:15]
        self._mock_consumer(data)

        napi = Napi()
        with self.assertRaises(StopIteration):
            msg = napi.next_message()

    def test_updates(self):
        self._mock_pika()
        self._mock_vip()
        data = self._open_message()[0:3]
        data_ret = self._open_return_message()[0:3]
        self._mock_consumer(data)

        napi = Napi()
        for i in range(3):
            msg = napi.updates()
            self.assertDictEqual(msg[0], data_ret[i])

        with self.assertRaises(StopIteration):
            msg = napi.updates()

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

    def _mock_consumer(self, data):
        napi_mock = patch(
            'globomap_driver_napi.rabbitmq.RabbitMQClient._consumer').start()
        napi_mock.return_value = iter(data)

    def _open_return_message(self):
        data = open_json('tests/json/update_messages.json')
        return data

    def _open_message(self):
        data = open_json('tests/json/queue_messages.json')
        return data


if __name__ == '__main__':
    unittest2.main()
