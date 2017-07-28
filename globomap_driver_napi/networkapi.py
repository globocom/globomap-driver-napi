from networkapiclient.ClientFactory import ClientFactory

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

        response = self.client.create_api_pool().get(
            ids=[pool_id], kind='details')
        pools = response.get('server_pools')
        if pools:
            return pools[0]

    def get_pool_by_member_id(self, member_id):
        """Return Pool"""

        response = self.client.create_api_vip_request().search(search={
            'extends_search': [{
                'serverpoolmember': member_id
            }]}, kind='details')

        pools = response.get('server_pools')
        if pools:
            return pools[0]

    def get_vip(self, vip_id):
        """Return VIP"""

        response = self.client.create_api_vip_request().get(
            ids=[vip_id], kind='details')
        vips = response.get('vips')
        if vips:
            return vips[0]

    def get_vip_by_portpool_id(self, portpool_id):
        """Return VIP"""

        response = self.client.create_api_vip_request().search(search={
            'extends_search': [{
                'viprequestport__viprequestportpool': portpool_id
            }]}, kind='details')

        vips = response.get('vips')
        if vips:
            return vips[0]
