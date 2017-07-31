import unittest2
from mock import MagicMock
from mock import patch

from globomap_driver_napi.networkapi import NetworkAPI


class TestNetworkAPI(unittest2.TestCase):

    def test_get_vip(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiVipRequest.get').start()
        requests_mock.return_value = {'vips': [{'id': 1}]}

        napi = NetworkAPI()
        napi.get_vip(1)
        requests_mock.assert_called_once_with(ids=[1], kind='details')

    def test_get_pool_by_member_id(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiPool.search').start()
        requests_mock.return_value = {'server_pools': [{'id': 1}]}

        napi = NetworkAPI()
        napi.get_pool_by_member_id(1)
        requests_mock.assert_called_once_with(
            search={'extends_search': [{'serverpoolmember': 1}]}, kind='details')

    def test_get_pool(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiPool.get').start()
        requests_mock.return_value = {'server_pools': [{'id': 1}]}

        napi = NetworkAPI()
        napi.get_pool(1)
        requests_mock.assert_called_once_with(ids=[1], kind='details')

    def test_get_vip_by_portpool_id(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiVipRequest.search').start()
        requests_mock.return_value = {'vips': [{'id': 1}]}

        napi = NetworkAPI()
        napi.get_vip_by_portpool_id(1)
        requests_mock.assert_called_once_with(
            search={'extends_search': [
                {'viprequestport__viprequestportpool': 1}]},
            kind='details')

    def test_get_network_ipv4_id(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiNetworkIPv4.get').start()
        requests_mock.return_value = {'networks': [{'id': 1}]}

        napi = NetworkAPI()
        napi.get_network_ipv4_id(1)
        requests_mock.assert_called_once_with(
            ids=[1],
            fields=['id', 'network_type__details',
                    'active', 'networkv4', 'vlan']
        )

    def test_get_network_ipv6_id(self):
        requests_mock = patch(
            'networkapiclient.ClientFactory.ApiNetworkIPv6.get').start()
        requests_mock.return_value = {'networks': [{'id': 1}]}

        napi = NetworkAPI()
        napi.get_network_ipv6_id(1)
        requests_mock.assert_called_once_with(
            ids=[1],
            fields=['id', 'network_type__details',
                    'active', 'networkv6', 'vlan']
        )


if __name__ == '__main__':
    unittest2.main()
