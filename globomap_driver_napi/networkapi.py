from networkapiclient.ClientFactory import ClientFactory
from networkapiclient.exception import NetworkAPIClientError

from.settings import NETWORKAPI_ENDPOINT
from.settings import NETWORKAPI_PASSWORD
from.settings import NETWORKAPI_USER


class NetworkAPI(object):

    def __init__(self):
        self.client = ClientFactory(
            NETWORKAPI_ENDPOINT, NETWORKAPI_USER, NETWORKAPI_PASSWORD
        )

    def get_pool(self, pool_id):
        """Return Pool"""

        try:
            response = self.client.create_api_pool().get(
                ids=[pool_id], kind='details')
        except NetworkAPIClientError:
            return []
        else:
            pools = response.get('server_pools')
            if pools:
                pools = pools[0]
            return pools

    def get_pool_by_member_id(self, member_id):
        """Return Pool"""

        response = self.client.create_api_pool().search(search={
            'extends_search': [{
                'serverpoolmember': member_id
            }]}, kind='details')

        pools = response.get('server_pools')
        if pools:
            pools = pools[0]
        return pools

    def get_vip(self, vip_id):
        """Return VIP"""

        try:
            response = self.client.create_api_vip_request().get(
                ids=[vip_id], kind='details')
            vips = response.get('vips')
        except NetworkAPIClientError:
            return []
        else:
            if vips:
                vips = vips[0]
            return vips

    def get_vip_by_portpool_id(self, portpool_id):
        """Return VIP"""

        response = self.client.create_api_vip_request().search(search={
            'extends_search': [{
                'viprequestport__viprequestportpool': portpool_id
            }]}, kind='details')

        vips = response.get('vips')
        if vips:
            vips = vips[0]
        return vips

    def get_network_ipv4_id(self, net_id):
        """Return NetworkIpv4"""

        try:
            response = self.client.create_api_network_ipv4().get(
                ids=[net_id],
                fields=['id', 'network_type__details',
                        'active', 'networkv4', 'vlan'])
        except NetworkAPIClientError:
            return []
        else:
            networks = response.get('networks')
            if networks:
                networks = networks[0]
            return networks

    def get_network_ipv6_id(self, net_id):
        """Return NetworkIpv6"""

        try:
            response = self.client.create_api_network_ipv6().get(
                ids=[net_id],
                fields=['id', 'network_type__details',
                        'active', 'networkv6', 'vlan'])
        except NetworkAPIClientError:
            return []
        else:
            networks = response.get('networks')
            if networks:
                networks = networks[0]
            return networks
