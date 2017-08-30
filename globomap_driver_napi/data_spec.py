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
            'properties': [
                {
                    'key': 'created',
                    'value': vip['created'],
                    'description': 'Created id Load Balancer'
                },
                {
                    'key': 'ip',
                    'value': ip_formated,
                    'description': 'IP'
                },
                {
                    'key': 'environmentvip',
                    'value': envvip,
                    'description': 'Environment of VIP'
                }
            ]
        }

        return data

    def port(self, port, vip_id):
        """Prepare dict of port to send"""

        self._validate(port)

        l7_value = port.get('l7_value')
        name = '{}:{}'.format(port['port'], l7_value) \
            if l7_value else port['port']
        data = {
            'from': 'vip/napi_{}'.format(vip_id),
            'to': 'pool/napi_{}'.format(port['server_pool']['id']),
            'id': str(port['id']),
            'name': str(name),
            'provider': 'napi'
        }

        return data

    def pool(self, pool):
        """Prepare dict of Pool to send"""

        self._validate(pool)

        data = {
            'id': str(pool['id']),
            'name': pool['identifier'],
            'provider': 'napi',
            'properties': [
                {
                    'key': 'default_port',
                    'value': pool['default_port'],
                    'description': 'Default Port of Pool'
                },
                {
                    'key': 'environment',
                    'value': pool['environment']['name'],
                    'description': 'Environment of Pool'
                },
                {
                    'key': 'servicedownaction',
                    'value': pool['servicedownaction']['name'],
                    'description': 'Action On Service Down'
                },
                {
                    'key': 'healthcheck',
                    'value': pool['healthcheck']['healthcheck_type'],
                    'description':'Healthcheck Type'
                },
                {
                    'key': 'lb_method',
                    'value': pool['lb_method'],
                    'description':'Method of Load Balancing'
                },
                {
                    'key': 'default_limit',
                    'value': pool['default_limit'],
                    'description':'Limit of Connections'
                },
                {
                    'key': 'pool_created',
                    'value': pool['pool_created'],
                    'description':'Created in Load Balancer'
                }
            ]
        }
        return data

    def pool_comp_unit(self, member, pool_id):
        """Prepare dict of Member to send."""

        self._validate(member)

        ip_formated = member['ip']['ip_formated'] \
            if member['ip'] else member['ipv6']['ip_formated']
        name = member.get('identifier') or ip_formated
        data = {
            'from': 'pool/napi_{}'.format(pool_id),
            'to': 'comp_unit/globomap_{}'.format(member['equipment']['name'].lower()),
            'id': str(member['id']),
            'name': name,
            'provider': 'napi',
            'properties': [
                {
                    'key': 'ip',
                    'value': ip_formated,
                    'description': 'IP'
                },
                {
                    'key': 'priority',
                    'value': member['priority'],
                    'description': 'Priority'
                },
                {
                    'key': 'weight',
                    'value': member['weight'],
                    'description': 'Weight'
                },
                {
                    'key': 'limit',
                    'value': member['limit'],
                    'description': 'Limit'
                },
                {
                    'key': 'port_real',
                    'value': member['port_real'],
                    'description': 'Port'
                }
            ]
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
            'properties': [
                {
                    'key': 'maintenance',
                    'value': compunit['maintenance'],
                    'description': 'Maintenance'
                },
                {
                    'key': 'equipment_type',
                    'value': compunit['equipment_type']['equipment_type'],
                    'description': 'Equipment Type'
                },
                {
                    'key': 'ips',
                    'value': ips,
                    'description': 'IPs'
                },
            ]
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
            'properties': [
                {
                    'key': 'active',
                    'value': network['active'],
                    'description': 'Network Status'
                },
                {
                    'key': 'network_type',
                    'value': network['network_type']['tipo_rede'],
                    'description': 'Network Type'
                }
            ]
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
            'properties': [
                {
                    'key': 'num_vlan',
                    'value': vlan['num_vlan'],
                    'description': 'Number of VLAN'
                },
                {
                    'key': 'description',
                    'value': vlan['description'],
                    'description': 'Description'
                },
                {
                    'key': 'active',
                    'value': vlan['active'],
                    'description': 'Status'
                }
            ]
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
            'properties': [
                {
                    'key': 'default_vrf',
                    'value': vrf,
                    'description': 'Default VRF'
                }
            ]
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
