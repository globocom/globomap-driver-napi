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
import logging

from networkapiclient.ClientFactory import ClientFactory
from networkapiclient.exception import NetworkAPIClientError

from.settings import NETWORKAPI_ENDPOINT
from.settings import NETWORKAPI_PASSWORD
from.settings import NETWORKAPI_USER


class NetworkAPI(object):

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.client = ClientFactory(
            NETWORKAPI_ENDPOINT, NETWORKAPI_USER, NETWORKAPI_PASSWORD
        )

    def _log_debug_request(self, func, param_id):
        self.logger.debug('[DriverNapi][request] %s %s' % (func, param_id))

    def _log_debug_response(self, func, param_id, response):
        self.logger.debug('[DriverNapi][response] %s %s/n%s' %
                          (func, param_id, response))

    def _log_warning_response(self, func, param_id, response):
        self.logger.warning(
            '[DriverNapi][response] %s %s/n%s' % (func, param_id, response))

    def get_pool(self, pool_id):
        """Return Pool"""

        try:
            response = self.client.create_api_pool().get(
                ids=[pool_id], kind='details')

        except NetworkAPIClientError as err:
            self._log_warning_response('get_pool', pool_id, err)
            return []

        else:
            self._log_debug_response('get_pool', pool_id, response)

            pools = response.get('server_pools')
            if pools:
                pools = pools[0]
            return pools

    def get_pool_by_member_id(self, member_id):
        """Return Pool by member id"""

        self._log_debug_request('get_pool_by_member_id', member_id)

        try:
            response = self.client.create_api_pool().search(search={
                'extends_search': [{
                    'serverpoolmember': member_id
                }]}, kind='details')

        except NetworkAPIClientError as err:
            self._log_warning_response('get_pool_by_member_id', member_id, err)
            return []

        else:
            self._log_debug_response(
                'get_pool_by_member_id', member_id, response)

            pools = response.get('server_pools')
            if pools:
                pools = pools[0]
            return pools

    def get_vip(self, vip_id):
        """Return VIP"""

        self._log_debug_request('get_vip', vip_id)

        try:
            response = self.client.create_api_vip_request().get(
                ids=[vip_id], kind='details')

        except NetworkAPIClientError as err:
            self._log_warning_response('get_vip', vip_id, err)
            return []

        else:
            self._log_debug_response('get_vip', vip_id, response)

            vips = response.get('vips')
            if vips:
                vips = vips[0]
            return vips

    def get_vip_by_portpool_id(self, portpool_id):
        """Return VIP by port pool id"""

        self._log_debug_request('get_vip_by_portpool_id', portpool_id)

        try:
            response = self.client.create_api_vip_request().search(search={
                'extends_search': [{
                    'viprequestport__viprequestportpool': portpool_id
                }]}, kind='details')

        except NetworkAPIClientError as err:
            self._log_warning_response(
                'get_vip_by_portpool_id', portpool_id, err)
            return []

        else:
            self._log_debug_response(
                'get_vip_by_portpool_id', portpool_id, response)

            vips = response.get('vips')
            if vips:
                vips = vips[0]
            return vips

    def get_equipment(self, equipment_id):
        """Return Equipment"""

        self._log_debug_request('get_equipment', equipment_id)

        try:
            response = self.client.create_api_equipment().get(
                ids=[equipment_id],
                include=[
                    'equipment_type__details',
                    'ipv4__basic__networkipv4',
                    'ipv6__basic__networkipv6'])

        except NetworkAPIClientError as err:
            self._log_warning_response('get_equipment', equipment_id, err)
            return []

        else:
            self._log_debug_response('get_equipment', equipment_id, response)

            equipments = response.get('equipments')
            if equipments:
                equipments = equipments[0]
            return equipments

    def get_network_ipv4_id(self, net_id):
        """Return NetworkIpv4"""

        self._log_debug_request('get_network_ipv4_id', net_id)

        try:
            response = self.client.create_api_network_ipv4().get(
                ids=[net_id],
                fields=['id', 'network_type__details',
                        'active', 'networkv4', 'vlan__basic'])

        except NetworkAPIClientError as err:
            self._log_warning_response('get_network_ipv4_id', net_id, err)
            return []

        else:
            self._log_debug_response('get_network_ipv4_id', net_id, response)

            networks = response.get('networks')
            if networks:
                networks = networks[0]
            return networks

    def get_network_ipv6_id(self, net_id):
        """Return NetworkIpv6"""

        self._log_debug_request('get_network_ipv4_id', net_id)

        try:
            response = self.client.create_api_network_ipv6().get(
                ids=[net_id],
                fields=['id', 'network_type__details',
                        'active', 'networkv6', 'vlan__basic'])

        except NetworkAPIClientError as err:
            self._log_warning_response('get_network_ipv4_id', net_id, err)
            return []

        else:
            self._log_debug_response('get_network_ipv4_id', net_id, response)

            networks = response.get('networks')
            if networks:
                networks = networks[0]
            return networks

    def get_ipv4_by_ip_equipment_id(self, ip_equipment_id):
        """Return Ipv4 by ip equipment id"""

        self._log_debug_request('get_ipv4_by_ip_equipment_id', ip_equipment_id)

        try:
            response = self.client.create_api_ipv4().search(
                search={'extends_search': [
                    {'ipequipamento': ip_equipment_id}]},
                fields=['networkipv4', 'ip_formated']
            )

        except NetworkAPIClientError as err:
            self._log_warning_response(
                'get_ipv4_by_ip_equipment_id', ip_equipment_id, err)
            return []

        else:
            self._log_debug_response(
                'get_ipv4_by_ip_equipment_id', ip_equipment_id, response)

            ips = response.get('ips')
            if ips:
                ips = ips[0]
            return ips

    def get_ipv6_by_ip_equipment_id(self, ip_equipment_id):
        """Return Ipv6 by ip equipment id"""

        self._log_debug_request('get_ipv6_by_ip_equipment_id', ip_equipment_id)

        try:
            response = self.client.create_api_ipv6().search(
                search={'extends_search': [
                    {'ipv6equipament': ip_equipment_id}]},
                fields=['networkipv6', 'ip_formated']
            )

        except NetworkAPIClientError as err:
            self._log_warning_response(
                'get_ipv6_by_ip_equipment_id', ip_equipment_id, err)
            return []

        else:
            self._log_debug_response(
                'get_ipv6_by_ip_equipment_id', ip_equipment_id, response)

            ips = response.get('ips')
            if ips:
                ips = ips[0]
            return ips

    def get_vlan(self, vlan_id):
        """Return Vlan"""

        self._log_debug_request('get_vlan', vlan_id)

        try:
            response = self.client.create_api_vlan().get(
                ids=[vlan_id], include=['environment__basic'])

        except NetworkAPIClientError as err:
            self._log_warning_response('get_vlan', vlan_id, err)
            return []

        else:
            self._log_debug_response('get_vlan', vlan_id, response)

            vlans = response.get('vlans')
            if vlans:
                vlans = vlans[0]
            return vlans

    def get_environment(self, environment_id):
        """Return Environment"""

        self._log_debug_request('get_environment', environment_id)

        try:
            response = self.client.create_api_environment().get(
                ids=[environment_id],
                include=['default_vrf__details', 'father_environment__basic']
            )

        except NetworkAPIClientError as err:
            self._log_warning_response('get_environment', environment_id, err)
            return []

        else:
            self._log_debug_response(
                'get_environment', environment_id, response)

            environments = response.get('environments')
            if environments:
                environments = environments[0]
            return environments
