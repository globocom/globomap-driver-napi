"""
   Copyright 2018 Globo.com

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
import unittest2
from mock import MagicMock
from mock import patch

from globomap_driver_napi.driver import Napi
from tests.util import open_json


class TestDriver(unittest2.TestCase):

    maxDiff = None

    def tearDown(self):
        patch.stopall()

    def test_method_not_exists(self):
        self._mock_pika()
        with self.assertRaises(AttributeError):
            kind = {
                'package': 'globomap_driver_napi.kind',
                'class': 'Kind',
                'method': 'not_exists',
            }
            self._create_driver()._processing_message(kind, None)

    def test_package_not_exists(self):
        self._mock_pika()
        with self.assertRaises(ImportError):
            kind = {
                'package': 'globomap_driver_napi.not_exists',
                'class': 'Kind',
                'method': 'vip',
            }
            self._create_driver()._processing_message(kind, None)

    def test_class_not_exists(self):
        self._mock_pika()
        with self.assertRaises(AttributeError):
            kind = {
                'package': 'globomap_driver_napi.kind',
                'class': 'NotExists',
                'method': 'vip',
            }
            self._create_driver()._processing_message(kind, None)

    def test_process_updates_vuln_comp_unit(self):
        rabbit_client_mock = self._mock_rabbitmq_client(
            open_json('tests/json/driver/queue/vip.json'))

        self._mock_vip()

        def callback(update):
            self.assertEquals('CREATE', update['action'])
            self.assertEquals('vip', update['collection'])
            self.assertEquals('collections', update['type'])

        self._create_driver().process_updates(callback)

        self.assertEqual(1, rabbit_client_mock.ack_message.call_count)
        self.assertEqual(0, rabbit_client_mock.nack_message.call_count)

    def test_process_updates_given_exception(self):
        rabbit_client_mock = self._mock_rabbitmq_client(
            open_json('tests/json/driver/queue/vip.json'))

        self._mock_vip()

        def callback(update):
            raise Exception()

        with self.assertRaises(Exception):
            self._create_driver().process_updates(callback)

        self.assertEqual(0, rabbit_client_mock.ack_message.call_count)
        self.assertEqual(1, rabbit_client_mock.nack_message.call_count)

    #########
    # MOCKS #
    #########
    def _mock_pika(self):
        patch('globomap_driver_napi.driver.pika.BlockingConnection').start()

    def _mock_vip(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vip').start()
        napi_mock.return_value = open_json(
            'tests/json/driver/networkapi/vip.json')

    def _mock_ipv4(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_ipv4').start()
        napi_mock.return_value = [{'equipments': [{'name': 'test'}]}]

    def _mock_rabbitmq_client(self, data=None):
        rabbit_mq_mock = patch(
            'globomap_driver_napi.driver.RabbitMQClient').start()
        rabbit = MagicMock()
        rabbit_mq_mock.return_value = rabbit
        rabbit.get_message.side_effect = [(data, 1), (None, None)]
        return rabbit

    def _create_driver(self):
        driver = Napi()
        return driver
