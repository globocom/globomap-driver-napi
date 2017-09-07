"""
   Copyright 2017 Globo.com

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
# -*- coding: utf-8 -*-


class DataSpec(object):

    """Class to prepare dicts"""

    def _validate(self, data):
        if not isinstance(data, dict):
            raise Exception('Param is not dict {}'.format(data))

    def vip(self, vip):
        """Prepare dict of VIP to send."""

        self._validate(vip)

        ip_formated = vip['ipv4']['ip_formated'] \
            if vip['ipv4'] else vip['ipv6']['ip_formated']
        envvip = vip['environmentvip']
        envvip = '{}-{}-{}'.format(envvip['finalidade_txt'],
                                   envvip['cliente_txt'],
                                   envvip['ambiente_p44_txt'])
        data = {
            'id': str(vip['id']),
            'name': vip['name'],
            'provider': 'napi',
            'properties': {
                'created': vip['created'],
                'ip': ip_formated,
                'environmentvip': envvip
            },
            'properties_metadata': {
                'created': {
                    'description': 'Created id Load Balancer'
                },
                'ip': {
                    'description': 'IP'
                },
                'environmentvip': {
                    'description': 'Environment of VIP'
                }
            }
        }

        return data

    def port(self, port, vip_id):
        """Prepare dict of port to send"""

        self._validate(port)
        if port['l7_rule']['nome_opcao_txt'] == 'default_vip':
            l7_value = 'Default VIP'
        elif port['l7_rule']['nome_opcao_txt'] == 'default_glob':
            l7_value = 'Default Rule'
        else:
            l7_value = port.get('l7_value')
        name = '{}:{}'.format(port['port'], l7_value) \
            if l7_value else port['port']
        data = {
            'from': 'vip/napi_{}'.format(vip_id),
            'to': 'pool/napi_{}'.format(port['server_pool']['id']),
            'id': str(port['id']),
            'name': str(name),
            'provider': 'napi',
            'properties': {
                'l4_protocol': port['options']['l4_protocol']['nome_opcao_txt'],
                'l7_protocol': port['options']['l7_protocol']['nome_opcao_txt'],
                'l7_rule': l7_value,
                'port': port['port']
            },
            'properties_metadata': {
                'l4_protocol': {
                    'description': 'L4 Protocol'
                },
                'l7_protocol': {
                    'description': 'L7 Protocol'
                },
                'l7_rule': {
                    'description': 'L7 Rule'
                },
                'port': {
                    'description': 'Port'
                }
            }
        }

        return data

    def pool(self, pool):
        """Prepare dict of Pool to send"""

        self._validate(pool)

        data = {
            'id': str(pool['id']),
            'name': pool['identifier'],
            'provider': 'napi',
            'properties': {
                'default_port': pool['default_port'],
                'environment': pool['environment']['name'],
                'servicedownaction': pool['servicedownaction']['name'],
                'healthcheck': pool['healthcheck']['healthcheck_type'],
                'lb_method': pool['lb_method'],
                'default_limit': pool['default_limit'],
                'pool_created': pool['pool_created']
            },
            'properties_metadata': {
                'default_port': {
                    'description': 'Default Port of Pool'
                },
                'environment': {
                    'description': 'Environment of Pool'
                },
                'servicedownaction': {
                    'description': 'Action On Service Down'
                },
                'healthcheck': {
                    'description': 'Healthcheck Type'
                },
                'lb_method': {
                    'description': 'Method of Load Balancing'
                },
                'default_limit': {
                    'description': 'Limit of Connections'
                },
                'pool_created': {
                    'description': 'Created in Load Balancer'
                }
            }
        }
        return data

    def pool_comp_unit(self, member, pool_id):
        """Prepare dict of Member to send."""

        self._validate(member)

        ip_formated = member['ip']['ip_formated'] \
            if member['ip'] else member['ipv6']['ip_formated']
        name = member.get('identifier') or ip_formated
        monitor = 'Up' if str(member['member_status']) in '1357' else 'Down'
        session = 'Up' if str(member['member_status']) in '2367' else 'Down'
        healthcheck = 'Up' if str(
            member['member_status']) in '4567' else 'Down'

        data = {
            'from': 'pool/napi_{}'.format(pool_id),
            'to': 'comp_unit/globomap_{}'.format(member['equipment']['name'].lower()),
            'id': str(member['id']),
            'name': name,
            'provider': 'napi',
            'properties': {
                'ip': ip_formated,
                'priority': member['priority'],
                'weight': member['weight'],
                'limit': member['limit'],
                'port_real': member['port_real'],
                'status_last_update': member['last_status_update_formated'],
                'status_monitor': monitor,
                'status_session': session,
                'status_healthcheck': healthcheck
            },
            'properties_metadata': {
                'ip': {
                    'description': 'IP'
                },
                'priority': {
                    'description': 'Priority'
                },
                'weight': {
                    'description': 'Weight'
                },
                'limit': {
                    'description': 'Limit'
                },
                'port_real': {
                    'description': 'Port'
                },
                'status_last_update': {
                    'description': 'Last Update of Status'
                },
                'status_monitor': {
                    'description': 'User Up/Down (Forced)'
                },
                'status_session': {
                    'description': 'Enabled/Disabled'
                },
                'status_healthcheck': {
                    'description': 'Up/Down (Healthcheck)'
                }
            }
        }

        return data

    def comp_unit(self, compunit):
        """Prepare dict of compunit to send"""

        self._validate(compunit)

        ips = [ip['ip_formated'] for ip in compunit.get('ipv4', [])]
        ips += [ip['ip_formated'] for ip in compunit.get('ipv6', [])]

        data = {
            'id': compunit['name'].lower(),
            'name': '',
            'provider': 'globomap',
            'properties': {
                'maintenance': compunit['maintenance'],
                'equipment_type': compunit['equipment_type']['equipment_type'],
                'ips': ips
            },
            'properties_metadata': {
                'maintenance': {
                    'description': 'Maintenance'
                },
                'equipment_type': {
                    'description': 'Equipment Type'
                },
                'ips': {
                    'description': 'IPs'
                }
            }
        }

        return data

    def network(self, network):
        """Prepare dict of network to send"""
        self._validate(network)

        version = 'v4' if network.get('networkv4') else 'v6'
        net = network.get('networkv4', network.get('networkv6'))

        data = {
            'id': '{}_{}'.format(version, network['id']),
            'name': net,
            'provider': 'napi',
            'properties': {
                'active': network['active'],
                'network_type': network['network_type']['tipo_rede']
            },
            'properties_metadata': {
                'active': {
                    'description': 'Active Network'
                },
                'network_type': {
                    'description': 'Network Type'
                }
            }
        }

        return data

    def network_comp_unit(self, ip, name_eqpt, ipeqpt_id):
        """Prepare dict of network_comp_unit to send"""

        self._validate(ip)

        net = ip.get('networkipv4') if ip.get(
            'networkipv4') else ip.get('networkipv6')
        version = 'v4' if ip.get('networkipv4') else 'v6'
        name_eqpt = name_eqpt.lower()
        ip_formated = ip.get('ip_formated').lower()

        data = {
            'from': 'network/napi_{}_{}'.format(version, net),
            'to': 'comp_unit/globomap_{}'.format(name_eqpt),
            'id': '{}_{}'.format(version, ipeqpt_id),
            'name': '{} - {}'.format(ip_formated, name_eqpt),
            'provider': 'napi',
        }

        return data

    def vlan_network(self, network):
        """Prepare dict of vlan_network to send"""
        self._validate(network)

        version = 'v4' if network.get('networkv4') else 'v6'
        net = network.get('networkv4', network.get('networkv6'))

        _id = '{}_{}'.format(version, network['id'])
        name = '{} - {}'.format(network['vlan']['num_vlan'], net)

        data = {
            'from': 'vlan/napi_{}'.format(network['vlan']['id']),
            'to': 'network/napi_{}_{}'.format(version, network['id']),
            'id': _id,
            'name': name,
            'provider': 'napi',
        }

        return data

    def vlan(self, vlan):
        """Prepare dict of vlan to send"""
        self._validate(vlan)

        data = {
            'id': str(vlan['id']),
            'name': vlan['name'],
            'provider': 'napi',
            'properties': {
                'num_vlan': vlan['num_vlan'],
                'description': vlan['description'],
                'active': vlan['active']
            },
            'properties_metadata': {
                'num_vlan': {
                    'description': 'Number of VLAN'
                },
                'description': {
                    'description': 'Description'
                },
                'active': {
                    'description': 'Active Vlan'
                }
            }
        }

        return data

    def environment_vlan(self, vlan):
        """Prepare dict of environment_vlan to send"""

        self._validate(vlan)
        data = {
            'from': 'environment/napi_{}'.format(vlan['environment']['id']),
            'to': 'vlan/napi_{}'.format(vlan['id']),
            'id': str(vlan['id']),
            'name': '{} / {}'.format(vlan['environment']['name'], vlan['num_vlan']),
            'provider': 'napi',
        }

        return data

    def environment(self, environment):
        """Prepare dict of environment to send"""
        self._validate(environment)
        vrf = environment['default_vrf'].get('vrf') \
            if environment['default_vrf']['vrf'] else ''
        data = {
            'id': str(environment['id']),
            'name': environment['name'],
            'provider': 'napi',
            'properties': {
                'default_vrf': vrf
            },
            'properties_metadata': {
                'default_vrf': {
                    'description': 'Default VRF'
                }
            }
        }

        return data

    def father_environment(self, environment):
        """Prepare dict of father_environment to send"""

        father_env = environment['father_environment']
        self._validate(environment)
        data = {
            'from': 'environment/napi_{}'.format(father_env['id']),
            'to': 'environment/napi_{}'.format(environment['id']),
            'id': str(environment['id']),
            'name': '{} / {}'.format(environment['name'], father_env['name']),
            'provider': 'napi',
        }

        return data
