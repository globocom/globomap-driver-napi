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
from mock import patch

from globomap_driver_napi.kind import Kind
from tests.util import open_json


class TestKind(unittest2.TestCase):

    maxDiff = None

    def tearDown(self):
        patch.stopall()

    def test_father_environment(self):
        self._mock_environment()

        data = self._queue_message(
            'tests/json/messages/queue/environment.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/father_environment.json')

        for i in range(3):
            kind = Kind()

            res = kind.father_environment(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_environment(self):
        self._mock_environment()

        data = self._queue_message(
            'tests/json/messages/queue/environment.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/environment.json')

        for i in range(3):
            kind = Kind()

            res = kind.environment(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_environment_vlan(self):
        self._mock_vlan()

        data = self._queue_message(
            'tests/json/messages/queue/vlan.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/environment_vlan.json')

        for i in range(3):
            kind = Kind()

            res = kind.environment_vlan(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_vlan(self):
        self._mock_vlan()

        data = self._queue_message(
            'tests/json/messages/queue/vlan.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/vlan.json')

        for i in range(3):
            kind = Kind()

            res = kind.vlan(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_vlan_networkv4(self):
        self._mock_networkv4()

        data = self._queue_message(
            'tests/json/messages/queue/networkv4.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/vlan_networkv4.json')

        for i in range(3):
            kind = Kind()

            res = kind.vlan_network_v4(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_vlan_networkv6(self):
        self._mock_networkv6()

        data = self._queue_message(
            'tests/json/messages/queue/networkv6.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/vlan_networkv6.json')

        for i in range(3):
            kind = Kind()

            res = kind.vlan_network_v6(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_networkv4(self):
        self._mock_networkv4()

        data = self._queue_message(
            'tests/json/messages/queue/networkv4.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/networkv4.json')

        for i in range(3):
            kind = Kind()

            res = kind.network_v4(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_networkv6(self):
        self._mock_networkv6()

        data = self._queue_message(
            'tests/json/messages/queue/networkv6.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/networkv6.json')

        for i in range(3):
            kind = Kind()

            res = kind.network_v6(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_ipv4_eqpt(self):
        self._mock_ipv4()

        data = self._queue_message(
            'tests/json/messages/queue/ipv4_eqpt.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/networkv4_comp_unit.json')

        for i in range(2):
            kind = Kind()

            res = kind.network_v4_comp_unit(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_ipv4_eqpt_acs(self):
        self._mock_ipv4()

        data = self._queue_message(
            'tests/json/messages/queue/ipv4_eqpt_acs.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/networkv4_comp_unit_acs.json')

        for i in range(2):
            kind = Kind()

            res = kind.network_v4_comp_unit(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_ipv6_eqpt(self):
        self._mock_ipv6()

        data = self._queue_message(
            'tests/json/messages/queue/ipv6_eqpt.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/networkv6_comp_unit.json')

        for i in range(2):
            kind = Kind()

            res = kind.network_v6_comp_unit(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_ipv6_eqpt_acs(self):
        self._mock_ipv6()

        data = self._queue_message(
            'tests/json/messages/queue/ipv6_eqpt_acs.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/networkv6_comp_unit_acs.json')

        for i in range(2):
            kind = Kind()

            res = kind.network_v6_comp_unit(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_comp_unit(self):
        self._mock_equipment()

        data = self._queue_message(
            'tests/json/messages/queue/equipment.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/comp_unit.json')

        for i in range(3):
            kind = Kind()

            res = kind.comp_unit(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_comp_unit_acs(self):
        self._mock_equipment_acs()

        data = self._queue_message(
            'tests/json/messages/queue/equipment_acs.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/comp_unit_acs.json')
        for i in range(3):
            kind = Kind()

            res = kind.comp_unit(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_vip(self):
        self._mock_vip()

        data = self._queue_message(
            'tests/json/messages/queue/vip_request.json')
        data_ret = self._update_message('tests/json/messages/updates/vip.json')

        for i in range(3):
            kind = Kind()

            res = kind.vip(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    # TODO
    # def test_vip_port(self):
    #     self._mock_vip_by_portpool_id()

    #     data = self._queue_message(
    #         'tests/json/messages/queue/vip_request_port.json')
    #     data_ret = self._update_message('tests/json/messages/updates/port.json')

    #     for i in range(3):
    #         kind = Kind()
    #         res = kind.port(data[i])
    #         self.assertDictEqual(res[0], data_ret[i])

    def test_port(self):
        self._mock_vip_by_portpool_id()

        data = self._queue_message(
            'tests/json/messages/queue/vip_request_port_pool.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/port.json')

        for i in range(3):
            kind = Kind()

            res = kind.port(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_pool(self):
        self._mock_pool()

        data = self._queue_message(
            'tests/json/messages/queue/server_pool.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/pool.json')

        for i in range(3):
            kind = Kind()

            res = kind.pool(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_pool_comp_unit(self):
        self._mock_pool_member_id()

        data = self._queue_message(
            'tests/json/messages/queue/server_pool_member.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/pool_comp_unit.json')

        for i in range(3):
            kind = Kind()

            res = kind.pool_comp_unit(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    def test_pool_comp_unit_acs(self):
        self._mock_pool_member_id_acs()

        data = self._queue_message(
            'tests/json/messages/queue/server_pool_member.json')
        data_ret = self._update_message(
            'tests/json/messages/updates/pool_comp_unit_acs.json')

        for i in range(3):
            kind = Kind()

            res = kind.pool_comp_unit(data[i])
            self.assertDictEqual(res[0], data_ret[i])

    ################
    # Non Existent #
    ################
    def test_vip_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vip').start()
        napi_mock.return_value = []
        data = self._queue_message(
            'tests/json/messages/queue/vip_request.json')

        kind = Kind()
        res = kind.vip(data[1])

        self.assertEqual(res, [])

    def test_port_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vip_by_portpool_id').start()
        napi_mock.return_value = []
        data = self._queue_message(
            'tests/json/messages/queue/vip_request_port_pool.json')

        kind = Kind()
        res = kind.port(data[1])

        self.assertEqual(res, [])

    def test_pool_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_pool').start()
        napi_mock.return_value = []
        data = self._queue_message(
            'tests/json/messages/queue/server_pool.json')

        kind = Kind()
        res = kind.pool(data[1])

        self.assertEqual(res, [])

    def test_pool_comp_unit_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_pool_by_member_id').start()
        napi_mock.return_value = []
        data = self._queue_message(
            'tests/json/messages/queue/server_pool_member.json')

        kind = Kind()
        res = kind.pool_comp_unit(data[1])

        self.assertEqual(res, [])

    def test_environment_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_environment').start()
        napi_mock.return_value = []
        data = self._queue_message(
            'tests/json/messages/queue/environment.json')

        kind = Kind()
        res = kind.environment(data[1])

        self.assertEqual(res, [])

    def test_father_environment_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_environment').start()
        napi_mock.return_value = []
        data = self._queue_message(
            'tests/json/messages/queue/environment.json')

        kind = Kind()
        res = kind.father_environment(data[1])

        self.assertEqual(res, [])

    def test_environment_vlan_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vlan').start()
        napi_mock.return_value = []
        data = self._queue_message('tests/json/messages/queue/vlan.json')

        kind = Kind()
        res = kind.environment_vlan(data[1])

        self.assertEqual(res, [])

    def test_vlan_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vlan').start()
        napi_mock.return_value = []
        data = self._queue_message('tests/json/messages/queue/vlan.json')

        kind = Kind()
        res = kind.vlan(data[1])

        self.assertEqual(res, [])

    def test_vlan_networkv4_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_network_ipv4_id').start()
        napi_mock.return_value = []
        data = self._queue_message('tests/json/messages/queue/networkv4.json')

        kind = Kind()
        res = kind.vlan_network_v4(data[1])

        self.assertEqual(res, [])

    def test_vlan_networkv6_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_network_ipv6_id').start()
        napi_mock.return_value = []
        data = self._queue_message('tests/json/messages/queue/networkv6.json')

        kind = Kind()
        res = kind.vlan_network_v6(data[1])

        self.assertEqual(res, [])

    def test_networkv4_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_network_ipv4_id').start()
        napi_mock.return_value = []
        data = self._queue_message('tests/json/messages/queue/networkv4.json')

        kind = Kind()
        res = kind.network_v4(data[1])

        self.assertEqual(res, [])

    def test_networkv6_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_network_ipv6_id').start()
        napi_mock.return_value = []
        data = self._queue_message('tests/json/messages/queue/networkv6.json')

        kind = Kind()
        res = kind.network_v6(data[1])

        self.assertEqual(res, [])

    def test_network_v4_comp_unit_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_ipv4_by_ip_equipment_id').start()
        napi_mock.return_value = []
        data = self._queue_message('tests/json/messages/queue/ipv4_eqpt.json')

        kind = Kind()
        res = kind.network_v4_comp_unit(data[0])

        self.assertEqual(res, [])

    def test_network_v6_comp_unit_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_ipv6_by_ip_equipment_id').start()
        napi_mock.return_value = []
        data = self._queue_message('tests/json/messages/queue/ipv6_eqpt.json')

        kind = Kind()
        res = kind.network_v6_comp_unit(data[0])

        self.assertEqual(res, [])

    def test_comp_unit_non_existent(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_equipment').start()
        napi_mock.return_value = []
        data = self._queue_message('tests/json/messages/queue/equipment.json')

        kind = Kind()
        res = kind.comp_unit(data[0])

        self.assertEqual(res, [])

    def test_network_v4_comp_unit_update(self):
        kind = Kind()
        res = kind.network_v4_comp_unit({
            'action': 'Alterar',
            'data': {'id_object': 1}
        })

        self.assertEqual(res, [])

    def test_network_v6_comp_unit_update(self):
        kind = Kind()
        res = kind.network_v6_comp_unit({
            'action': 'Alterar',
            'data': {'id_object': 1}
        })

        self.assertEqual(res, [])

    #########
    # MOCKS #
    #########
    def _mock_environment(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_environment').start()
        data = open_json('tests/json/messages/networkapi/get_environment.json')
        napi_mock.return_value = data['environments'][0]

    def _mock_vlan(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vlan').start()
        data = open_json('tests/json/messages/networkapi/get_vlan.json')
        napi_mock.return_value = data['vlans'][0]

    def _mock_networkv4(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_network_ipv4_id').start()
        data = open_json('tests/json/messages/networkapi/get_networkv4.json')
        napi_mock.return_value = data['networks'][0]

    def _mock_networkv6(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_network_ipv6_id').start()
        data = open_json('tests/json/messages/networkapi/get_networkv6.json')
        napi_mock.return_value = data['networks'][0]

    def _mock_ipv4(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_ipv4_by_ip_equipment_id').start()
        data = open_json('tests/json/messages/networkapi/get_ipv4.json')
        napi_mock.return_value = data['ips'][0]

    def _mock_ipv6(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_ipv6_by_ip_equipment_id').start()
        data = open_json('tests/json/messages/networkapi/get_ipv6.json')
        napi_mock.return_value = data['ips'][0]

    def _mock_equipment(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_equipment').start()
        data = open_json('tests/json/messages/networkapi/get_equipment.json')
        napi_mock.return_value = data['equipments'][0]

    def _mock_equipment_acs(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_equipment').start()
        data = open_json(
            'tests/json/messages/networkapi/get_equipment_acs.json')
        napi_mock.return_value = data['equipments'][0]

    def _mock_vip(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vip').start()
        data = open_json('tests/json/messages/networkapi/get_vip.json')
        napi_mock.return_value = data['vips'][0]

    def _mock_pool_member_id(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_pool_by_member_id').start()
        data = open_json('tests/json/messages/networkapi/get_pool.json')
        napi_mock.return_value = data['server_pools'][0]

    def _mock_pool_member_id_acs(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_pool_by_member_id').start()
        data = open_json('tests/json/messages/networkapi/get_pool_acs.json')
        napi_mock.return_value = data['server_pools'][0]

    def _mock_vip_by_portpool_id(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_vip_by_portpool_id').start()
        data = open_json('tests/json/messages/networkapi/get_vip.json')
        napi_mock.return_value = data['vips'][0]

    def _mock_pool(self):
        napi_mock = patch(
            'globomap_driver_napi.driver.NetworkAPI.get_pool').start()
        data = open_json('tests/json/messages/networkapi/get_pool.json')
        napi_mock.return_value = data['server_pools'][0]

    def _queue_message(self, file_name):
        data = open_json(file_name)
        return data

    def _update_message(self, file_name):
        data = open_json(file_name)
        return data


if __name__ == '__main__':
    unittest2.main()
