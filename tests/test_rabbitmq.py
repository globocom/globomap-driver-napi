import unittest

from mock import MagicMock
from mock import patch

from globomap_driver_napi.rabbitmq import RabbitMQClient


class TestRabbitMQClient(unittest.TestCase):

    def tearDown(self):
        patch.stopall()

    def test_get_message(self):
        pika_mock = self._mock_pika(
            '{"action": "CREATE", "type": "vip", "element": {}}')
        rabbitmq = RabbitMQClient(
            'localhost', 5672, 'user', 'password', '/', 'queue_name')

        message = rabbitmq.get_message()

        self.assertIsNotNone(message)
        pika_mock.basic_get.assert_called_once_with('queue_name')

    def _mock_pika(self, message):
        pika_mock = patch('globomap_driver_napi.rabbitmq.pika').start()

        pika_mock.ConnectionParameters.return_value = MagicMock()
        connection_mock = MagicMock()
        channel_mock = MagicMock()

        connection_mock.channel.return_value = channel_mock
        pika_mock.BlockingConnection.return_value = connection_mock
        channel_mock.basic_get.return_value = (MagicMock(), None, message)

        return channel_mock


if __name__ == '__main__':
    unittest2.main()
