import unittest2
from mock import MagicMock
from mock import Mock
from mock import patch

from globomap_driver_napi.networkapi import NetworkAPI
from globomap_driver_napi.networkapi import NetworkAPIClientError


class TestNetworkAPI(unittest2.TestCase):
    """Test using client networkapi"""

    def test_get_vip(self):
        """Test assert called get vip"""

        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiVipRequest.get').start()
        requests_mock.return_value = {'vips': [{'id': 1}]}

        napi = NetworkAPI()
        data = napi.get_vip(1)
        requests_mock.assert_called_once_with(ids=[1], kind='details')

        self.assertDictEqual(data, {'id': 1})

    def test_get_pool_by_member_id(self):
        """Test assert called get pool by member"""

        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiPool.search').start()
        requests_mock.return_value = {'server_pools': [{'id': 1}]}

        napi = NetworkAPI()
        data = napi.get_pool_by_member_id(1)
        requests_mock.assert_called_once_with(
            search={'extends_search': [{'serverpoolmember': 1}]}, kind='details')

        self.assertDictEqual(data, {'id': 1})

    def test_get_pool(self):
        """Test assert called get pool"""

        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiPool.get').start()
        requests_mock.return_value = {'server_pools': [{'id': 1}]}

        napi = NetworkAPI()
        data = napi.get_pool(1)
        requests_mock.assert_called_once_with(ids=[1], kind='details')

        self.assertDictEqual(data, {'id': 1})

    def test_get_vip_by_portpool_id(self):
        """Test assert called get vip by port"""

        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiVipRequest.search').start()
        requests_mock.return_value = {'vips': [{'id': 1}]}

        napi = NetworkAPI()
        data = napi.get_vip_by_portpool_id(1)
        requests_mock.assert_called_once_with(
            search={'extends_search': [
                {'viprequestport__viprequestportpool': 1}]},
            kind='details')

        self.assertDictEqual(data, {'id': 1})

    def test_get_network_ipv4_id(self):
        """Test assert called get network v4"""

        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiNetworkIPv4.get').start()
        requests_mock.return_value = {'networks': [{'id': 1}]}

        napi = NetworkAPI()
        data = napi.get_network_ipv4_id(1)
        requests_mock.assert_called_once_with(
            ids=[1],
            fields=['id', 'network_type__details',
                    'active', 'networkv4', 'vlan__basic']
        )

        self.assertDictEqual(data, {'id': 1})

    def test_get_network_ipv6_id(self):
        """Test assert called get network v6"""

        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiNetworkIPv6.get').start()
        requests_mock.return_value = {'networks': [{'id': 1}]}

        napi = NetworkAPI()
        data = napi.get_network_ipv6_id(1)
        requests_mock.assert_called_once_with(
            ids=[1],
            fields=['id', 'network_type__details',
                    'active', 'networkv6', 'vlan__basic']
        )

        self.assertDictEqual(data, {'id': 1})

    def test_get_environment(self):
        """Test assert called get environment"""

        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiEnvironment.get').start()
        requests_mock.return_value = {'environments': [{'id': 1}]}

        napi = NetworkAPI()
        data = napi.get_environment(1)
        requests_mock.assert_called_once_with(
            ids=[1], include=['default_vrf__details',
                              'father_environment__basic'])

        self.assertDictEqual(data, {'id': 1})

    def test_get_vlan(self):
        """Test assert called get vlan"""

        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiVlan.get').start()
        requests_mock.return_value = {'vlans': [{'id': 1}]}

        napi = NetworkAPI()
        data = napi.get_vlan(1)
        requests_mock.assert_called_once_with(
            ids=[1],
            include=['environment__basic']
        )

        self.assertDictEqual(data, {'id': 1})

    def test_get_ipv4_by_ip_equipment_id(self):
        """Test assert called get ipv4 by ip eqpt"""

        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiIPv4.search').start()
        requests_mock.return_value = {'ips': [{'id': 1}]}

        napi = NetworkAPI()
        data = napi.get_ipv4_by_ip_equipment_id(1)
        requests_mock.assert_called_once_with(
            search={'extends_search': [{'ipequipamento': 1}]},
            fields=['networkipv4', 'ip_formated']
        )

        self.assertDictEqual(data, {'id': 1})

    def test_get_ipv6_by_ip_equipment_id(self):
        """Test assert called get ipv6 by ip eqpt"""

        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiIPv6.search').start()
        requests_mock.return_value = {'ips': [{'id': 1}]}

        napi = NetworkAPI()
        data = napi.get_ipv6_by_ip_equipment_id(1)
        requests_mock.assert_called_once_with(
            search={'extends_search': [{'ipv6equipament': 1}]},
            fields=['networkipv6', 'ip_formated']
        )

        self.assertDictEqual(data, {'id': 1})

    def test_get_equipment(self):
        """Test assert called get equipment"""

        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiEquipment.get').start()
        requests_mock.return_value = {'equipments': [{'id': 1}]}

        napi = NetworkAPI()
        data = napi.get_equipment(1)
        requests_mock.assert_called_once_with(
            ids=[1],
            include=['equipment_type__details',
                     'ipv4__basic__networkipv4', 'ipv6__basic__networkipv6']
        )

        self.assertDictEqual(data, {'id': 1})

    def test_exception_get_pool(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiPool.get').start()
        requests_mock.side_effect = NetworkAPIClientError('')

        napi = NetworkAPI()
        data = napi.get_pool(3)
        self.assertEqual(data, [])

    def test_exception_get_pool_by_member_id(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiPool.search').start()
        requests_mock.side_effect = NetworkAPIClientError('')

        napi = NetworkAPI()

        data = napi.get_pool_by_member_id(3)
        self.assertEqual(data, [])

    def test_exception_get_vip(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiVipRequest.get').start()
        requests_mock.side_effect = NetworkAPIClientError('')

        napi = NetworkAPI()
        data = napi.get_vip(3)
        self.assertEqual(data, [])

    def test_exception_get_vip_by_portpool_id(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiVipRequest.search').start()
        requests_mock.side_effect = NetworkAPIClientError('')

        napi = NetworkAPI()

        data = napi.get_vip_by_portpool_id(3)
        self.assertEqual(data, [])

    def test_exception_get_equipment(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiEquipment.get').start()
        requests_mock.side_effect = NetworkAPIClientError('')

        napi = NetworkAPI()

        data = napi.get_equipment(3)
        self.assertEqual(data, [])

    def test_exception_get_network_ipv4_id(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiNetworkIPv4.get').start()
        requests_mock.side_effect = NetworkAPIClientError('')

        napi = NetworkAPI()

        data = napi.get_network_ipv4_id(3)
        self.assertEqual(data, [])

    def test_exception_get_network_ipv6_id(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiNetworkIPv6.get').start()
        requests_mock.side_effect = NetworkAPIClientError('')

        napi = NetworkAPI()

        data = napi.get_network_ipv6_id(3)
        self.assertEqual(data, [])

    def test_exception_get_ipv4_by_ip_equipment_id(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiIPv4.search').start()
        requests_mock.side_effect = NetworkAPIClientError('')

        napi = NetworkAPI()

        data = napi.get_ipv4_by_ip_equipment_id(3)
        self.assertEqual(data, [])

    def test_exception_get_ipv6_by_ip_equipment_id(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiIPv6.search').start()
        requests_mock.side_effect = NetworkAPIClientError('')

        napi = NetworkAPI()

        data = napi.get_ipv6_by_ip_equipment_id(3)
        self.assertEqual(data, [])

    def test_exception_get_vlan(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiVlan.get').start()
        requests_mock.side_effect = NetworkAPIClientError('')

        napi = NetworkAPI()
        data = napi.get_vlan(3)
        self.assertEqual(data, [])

    def test_exception_get_environment(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiEnvironment.get').start()
        requests_mock.side_effect = NetworkAPIClientError('')

        napi = NetworkAPI()

        data = napi.get_environment(3)
        self.assertEqual(data, [])
