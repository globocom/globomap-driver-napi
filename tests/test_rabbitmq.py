import json
import unittest

from mock import MagicMock
from mock import Mock
from mock import patch

from globomap_driver_napi.rabbitmq import RabbitMQClient
from tests.util import open_json


class TestRabbitMQClient(unittest.TestCase):

    def tearDown(self):
        patch.stopall()

    def setUp(self):
        self.pika_mock = self._mock_pika()

    def test_get_message(self):
        msg = '{"action": "CREATE", "type": "vip", "element": {}}'

        self.pika_mock.basic_get.return_value = (MagicMock(), None, msg)
        rabbitmq = RabbitMQClient('', '', '', '', '', 'queue_name')

        message = rabbitmq.get_message()

        self.assertIsNotNone(message)
        self.pika_mock.basic_get.assert_called_once_with('queue_name')

    def test_read_messages(self):
        msg = '{"action": "CREATE", "type": "vip", "element": {}}'

        self.pika_mock.basic_get.return_value = (MagicMock(), None, msg)
        rabbitmq = RabbitMQClient('', '', '', '', '', 'queue_name')

        for i in range(3):
            msg_ret = rabbitmq.read_messages().next()
            self.assertDictEqual(msg_ret[0], json.loads(msg))

    def test_read_two_messages(self):
        rabbitmq = RabbitMQClient('', '', '', '', '', 'queue_name')

        msgs = [
            {'action': 'CREATE', 'type': 'vip', 'element': {}},
            {'action': 'CREATE', 'type': 'pool', 'element': {}}
        ]
        rabbitmq.get_message = Mock(side_effect=msgs)
        msg_ret = rabbitmq.read_messages(2).next()

        self.assertEqual(len(msg_ret), 2)
        for i in range(2):
            self.assertDictEqual(msg_ret[i], msgs[i])

        with self.assertRaises(StopIteration):
            rabbitmq.read_messages().next()

    def test_read_tree_messages(self):
        rabbitmq = RabbitMQClient('', '', '', '', '', 'queue_name')

        msgs = [
            {'action': 'CREATE', 'type': 'vip', 'element': {}},
            {'action': 'CREATE', 'type': 'pool', 'element': {}}
        ]
        rabbitmq.get_message = Mock(side_effect=msgs)
        msg_ret = rabbitmq.read_messages(3).next()

        self.assertEqual(len(msg_ret), 2)
        for i in range(2):
            self.assertDictEqual(msg_ret[i], msgs[i])

        with self.assertRaises(StopIteration):
            rabbitmq.read_messages().next()

    def test_read_five_messages(self):
        rabbitmq = RabbitMQClient('', '', '', '', '', 'queue_name')

        msgs = [
            {'action': 'CREATE', 'type': 'vip', 'element': {}},
            {'action': 'CREATE', 'type': 'pool', 'element': {}},
            {'action': 'DELETE', 'type': 'pool', 'element': {}},
            {'action': 'UPDATE', 'type': 'pool', 'element': {}},
            {'action': 'UPDATE', 'type': 'vip', 'element': {}}
        ]
        rabbitmq.get_message = Mock(side_effect=msgs)
        msg_ret = rabbitmq.read_messages(3).next()

        self.assertEqual(len(msg_ret), 3)
        for i in range(3):
            self.assertDictEqual(msg_ret[i], msgs[i])

        msg_ret = rabbitmq.read_messages(3).next()

        self.assertEqual(len(msg_ret), 2)
        self.assertDictEqual(msg_ret[0], msgs[3])
        self.assertDictEqual(msg_ret[1], msgs[4])

        with self.assertRaises(StopIteration):
            rabbitmq.read_messages().next()

    def test_stop_read_messages(self):

        pika_mock = self._mock_pika()
        pika_mock.basic_get.return_value = (None, None, None)

        rabbitmq = RabbitMQClient(
            'localhost', 5672, 'user', 'password', '/', 'queue_name')

        with self.assertRaises(StopIteration):
            rabbitmq.read_messages().next()

    def _mock_pika(self):
        pika_mock = patch('globomap_driver_napi.rabbitmq.pika').start()

        pika_mock.ConnectionParameters.return_value = MagicMock()
        connection_mock = MagicMock()
        channel_mock = MagicMock()

        connection_mock.channel.return_value = channel_mock
        pika_mock.BlockingConnection.return_value = connection_mock

        return channel_mock
