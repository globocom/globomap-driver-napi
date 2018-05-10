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
import json
import logging
from time import time

from globomap_loader_api_client import auth
from globomap_loader_api_client.update import Update
from networkapiclient.exception import NetworkAPIClientError

from globomap_driver_napi import settings
from globomap_driver_napi.data_spec import DataSpec
from globomap_driver_napi.networkapi import NetworkAPI
from globomap_driver_napi.util import clear


class Loader(object):

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.search = {'asorting_cols': ['-id']}
        self.client = NetworkAPI().client
        auth_inst = auth.Auth(
            api_url=settings.GLOBOMAP_LOADER_API_URL,
            username=settings.GLOBOMAP_LOADER_API_USERNAME,
            password=settings.GLOBOMAP_LOADER_API_PASSWORD
        )
        self.update = Update(auth=auth_inst, driver_name='napi')

    def _construct(self, action, collection, type_coll, content):
        new_time = int(time())
        content['timestamp'] = new_time
        data = {
            'action': action,
            'collection': collection,
            'type': type_coll,
            'element': content
        }
        if action != 'CREATE':
            data['key'] = '{}_{}'.format(content['provider'], content['id'])

        return data

    def send(self, data):
        try:
            res = self.update.post(data)
        except Exception:
            self.logger.exception('Message dont sent %s', json.dumps(data))
        else:
            return res

    def vips(self):
        """Load vips"""
        data_list = []

        obj = self.client.create_api_vip_request()
        pages = self._paging(obj=obj, key='vips', next_search=self.search,
                             kind='details')
        while True:
            vips = next(pages)
            for vip in vips:
                data_list.append(self._vip(vip))
                data_list += self._ports(vip)

            res = data_list
            data_list = []
            yield res

    def pools(self):
        """Load pools"""
        data_list = []

        obj = self.client.create_api_pool()
        pages = self._paging(obj=obj, key='server_pools',
                             next_search=self.search, kind='details')
        while True:
            pools = next(pages)
            for pool in pools:
                data_list.append(self._pool(pool))
                data_list += self._pool_members(pool)

            res = data_list
            data_list = []
            yield res

    def equipments(self):
        """Load equipments"""
        data_list = []

        obj = self.client.create_api_v4_equipment()
        pages = self._paging(
            obj=obj, key='equipments', next_search=self.search,
            include=['ipsv4__basic__ip__ip_formated',
                     'ipsv6__basic__ip__ip_formated',
                     'equipment_type__details'])
        while True:
            equipments = next(pages)
            for equipment in equipments:
                data_list.append(self._equipament(equipment))
                data_list += self._equipment_ipv4(equipment)
                data_list += self._equipment_ipv6(equipment)

            res = data_list
            data_list = []
            yield res

    def networksv4(self):
        """Load networksv4"""
        data_list = []

        obj = self.client.create_api_network_ipv4()
        pages = self._paging(obj=obj, key='networks',
                             next_search=self.search, kind='details')
        while True:
            networks = next(pages)
            for network in networks:
                data_list.append(self._networkv4(network))
                data_list.append(self._network_vlan(network))

            res = data_list
            data_list = []
            yield res

    def networksv6(self):
        """Load networksv6"""
        data_list = []

        obj = self.client.create_api_network_ipv6()
        pages = self._paging(obj=obj, key='networks',
                             next_search=self.search, kind='details')
        while True:
            networks = next(pages)
            for network in networks:
                data_list.append(self._networkv6(network))
                data_list.append(self._network_vlan(network))

            res = data_list
            data_list = []
            yield res

    def vlans(self):
        """Load vlans"""
        data_list = []

        obj = self.client.create_api_vlan()
        pages = self._paging(obj=obj, key='vlans',
                             next_search=self.search,
                             include=['environment__basic'])
        while True:
            vlans = next(pages)
            for vlan in vlans:
                data_list.append(self._vlan(vlan))
                data_list.append(self._environment_vlan(vlan))

            res = data_list
            data_list = []
            yield res

    def environments(self):
        """Load environments"""
        data_list = []

        obj = self.client.create_api_environment()
        pages = self._paging(
            obj=obj, key='environments', next_search=self.search,
            include=['default_vrf__details', 'father_environment__basic'])

        while True:
            environments = next(pages)
            for environment in environments:
                data_list.append(self._environment(environment))
                if environment['father_environment']:
                    data_list.append(self._father_environment(environment))

            res = data_list
            data_list = []
            yield res

    def _vip(self, vip):
        content = DataSpec().vip(vip)
        data = self._construct('UPDATE', 'vip', 'collections', content)

        return data

    def _ports(self, vip):
        data_list = []
        for port in vip['ports']:
            for pool in port['pools']:
                pool['port'] = port['port']
                pool['options'] = port['options']
                content = DataSpec().port(pool, vip['id'])
                data = self._construct('UPDATE', 'port', 'edges', content)

                data_list.append(data)

        return data_list

    def _pool(self, pool):
        content = DataSpec().pool(pool)
        data = self._construct('UPDATE', 'pool', 'collections', content)

        return data

    def _pool_members(self, pool):
        data_list = []
        for member in pool.get('server_pool_members', []):

            content = DataSpec().pool_comp_unit(member, pool['id'])
            data = self._construct(
                'UPDATE', 'pool_comp_unit', 'edges', content)

            data_list.append(data)

        return data_list

    def _equipament(self, equipment):
        equipment['ipv4'] = [ip['ip'] for ip in equipment['ipsv4']]
        equipment['ipv6'] = [ip['ip'] for ip in equipment['ipsv6']]
        content = DataSpec().comp_unit(equipment)
        data = self._construct('PATCH', 'comp_unit', 'collections', content)

        return data

    def _equipment_ipv4(self, equipment):
        data_list = []
        for ipv4 in equipment.get('ipsv4'):
            ipv4['ip']['networkipv4'] = ipv4['ip']['networkipv4']['id']
            content = DataSpec().network_comp_unit(
                ipv4['ip'], equipment['name'], ipv4['id'])
            data = self._construct(
                'UPDATE', 'network_comp_unit', 'edges', content)
            data_list.append(data)

        return data_list

    def _equipment_ipv6(self, equipment):
        data_list = []
        for ipv6 in equipment.get('ipsv6'):
            ipv6['ip']['networkipv6'] = ipv6['ip']['networkipv6']['id']
            content = DataSpec().network_comp_unit(
                ipv6['ip'], equipment['name'], ipv6['id'])
            data = self._construct(
                'UPDATE', 'network_comp_unit', 'edges', content)
            data_list.append(data)

        return data_list

    def _networkv6(self, network):
        content = DataSpec().network(network)
        data = self._construct('UPDATE', 'network', 'collections', content)

        return data

    def _network_vlan(self, network):
        content = DataSpec().vlan_network(network)
        data = self._construct('UPDATE', 'vlan_network', 'edges', content)

        return data

    def _networkv4(self, network):
        content = DataSpec().network(network)
        data = self._construct('UPDATE', 'network', 'collections', content)

        return data

    def _vlan(self, vlan):
        content = DataSpec().vlan(vlan)
        data = self._construct('UPDATE', 'vlan', 'collections', content)

        return data

    def _environment_vlan(self, vlan):
        content = DataSpec().environment_vlan(vlan)
        data = self._construct('UPDATE', 'environment_vlan',
                               'edges', content)

        return data

    def _environment(self, environment):
        content = DataSpec().environment(environment)
        data = self._construct('UPDATE', 'environment',
                               'collections', content)

        return data

    def _father_environment(self, environment):
        content = DataSpec().father_environment(environment)
        data = self._construct('UPDATE', 'father_environment',
                               'edges', content)

        return data

    def _paging(self, **kwargs):

        obj = kwargs.get('obj')
        key = kwargs.get('key')
        next_search = kwargs.get('next_search')
        kind = kwargs.get('kind', '')
        fields = kwargs.get('fields', [])
        include = kwargs.get('include', [])

        while True:
            self.logger.debug(
                '[DriverNapi][loader][request] %s - next_search %s' %
                (key, next_search)
            )
            try:

                objs = obj.search(search=next_search, kind=kind,
                                  fields=fields, include=include)
            except NetworkAPIClientError as err:
                self.logger.error(
                    '[DriverNapi][loader][response] %s %s' % (key, err))
                break
            else:
                self.logger.debug(
                    '[DriverNapi][loader][response] %s %s' %
                    (key, objs[key])
                )
                if objs[key]:
                    next_search = objs['next_search']
                    yield objs[key]
                else:
                    break

    def run(self):
        current_time = int(time())

        for messages in self.vips():
            self.send(messages)

        for messages in self.pools():
            self.send(messages)

        for messages in self.environments():
            self.send(messages)

        for messages in self.vlans():
            self.send(messages)

        for messages in self.networksv4():
            self.send(messages)

        for messages in self.networksv6():
            self.send(messages)

        for messages in self.equipments():
            self.send(messages)

        self.send([clear('vip', 'collections', current_time)])
        self.send([clear('pool', 'collections', current_time)])
        self.send([clear('comp_unit', 'collections', current_time)])
        self.send([clear('network', 'collections', current_time)])
        self.send([clear('vlan', 'collections', current_time)])
        self.send([clear('environment', 'collections', current_time)])
        self.send([clear('port', 'edges', current_time)])
        self.send([clear('pool_comp_unit', 'edges', current_time)])
        self.send([clear('network_comp_unit', 'edges', current_time)])
        self.send([clear('vlan_network', 'edges', current_time)])
        self.send([clear('environment_vlan', 'edges', current_time)])
        self.send([clear('father_environment', 'edges', current_time)])
