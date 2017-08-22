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

    def test_method_not_exists(self):
        self._mock_pika()
        with self.assertRaises(AttributeError):
            napi = Napi()
            kind = {
                'package': 'globomap_driver_napi.kind',
                'class': 'Kind',
                'method': 'not_exists',
            }
            napi._treat_message(kind, None)

    def test_package_not_exists(self):
        self._mock_pika()
        with self.assertRaises(ImportError):
            napi = Napi()
            kind = {
                'package': 'globomap_driver_napi.not_exists',
                'class': 'Kind',
                'method': 'vip',
            }
            napi._treat_message(kind, None)

    def test_class_not_exists(self):
        self._mock_pika()
        with self.assertRaises(AttributeError):
            napi = Napi()
            kind = {
                'package': 'globomap_driver_napi.kind',
                'class': 'NotExists',
                'method': 'vip',
            }
            napi._treat_message(kind, None)

    def test_msg_dont_treated(self):
        self._mock_pika()
        napi = Napi()

        data = self._open_message()[0:1]
        self._mock_consumer(data)

        napi._treat_message = Mock(return_value=False)
        with self.assertRaises(StopIteration):
            napi.next_message()

    def test_ignore_get_messages(self):
        self._mock_pika()
        self._mock_pool()
        data = self._open_message()[3:]
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

    def test_updates_2_msg(self):
        self._mock_pika()
        self._mock_vip()
        data = self._open_message()[0:3]
        data_ret = self._open_return_message()[0:3]
        self._mock_consumer(data)

        napi = Napi()

        msg = napi.updates(2)
        for i in range(2):
            self.assertDictEqual(msg[i], data_ret[i])

        msg = napi.updates(2)
        self.assertDictEqual(msg[0], data_ret[2])

        with self.assertRaises(StopIteration):
            msg = napi.updates(2)

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

    def _mock_pool(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_pool').start()
        data = open_json('tests/json/driver/get_pool.json')
        napi_mock.return_value = data['server_pools'][0]

    def _mock_consumer(self, data):
        napi_mock = patch(
            'globomap_driver_napi.rabbitmq.RabbitMQClient._consumer').start()
        napi_mock.return_value = iter(data)

    def _open_return_message(self):
        data = open_json('tests/json/driver/update_messages.json')
        return data

    def _open_message(self):
        data = open_json('tests/json/driver/queue_messages.json')
        return data


if __name__ == '__main__':
    unittest2.main()
