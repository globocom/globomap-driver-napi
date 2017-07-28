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
                                   envvip['cliente_txt'], envvip['ambiente_p44_txt'])
        data = {
            'collection': 'vip',
            'content': {
                'id': vip['id'],
                'name': vip['name'],
                'properties': {
                    'created': vip['created'],
                    'ip': ip_formated,
                    'environmentvip': envvip
                }
            }
        }

        return data

    def port(self, port, vip_id):
        """Prepare dict of port to send"""

        self._validate(port)
        l7_value = port.get('l7_value')
        name = '{}:{}'.format(port['port'], l7_value) \
            if l7_value else port['port']
        data = {
            'collection': 'port',
            'from': {
                'collection': 'vip',
                'provider': 'napi',
                'id': vip_id
            },
            'to': {
                'collection': 'pool',
                'provider': 'napi',
                'id': port['server_pool']['id']
            },
            'content': {
                'id': port['id'],
                'name': str(name)
            }
        }

        return data

    def pool(self, pool):
        """Prepare dict of Pool to send"""

        self._validate(pool)
        data = {
            'collection': 'pool',
            'content': {
                'id': pool['id'],
                'name': pool['identifier'],
                'properties': {
                    'default_port': pool['default_port'],
                    'environment': pool['environment']['name'],
                    'servicedownaction': pool['servicedownaction']['name'],
                    'healthcheck': pool['healthcheck']['healthcheck_type'],
                    'lb_method': pool['lb_method'],
                    'default_limit': pool['default_limit'],
                    'pool_created': pool['pool_created']
                }
            }
        }
        return data

    def pool_comp_unit(self, member, pool_id):
        """Prepare dict of Member to send."""

        self._validate(member)
        ip_formated = member['ip']['ip_formated'] \
            if member['ip'] else member['ipv6']['ip_formated']
        data = {
            'collection': 'pool_comp_unit',
            'from': {
                'collection': 'pool',
                'provider': 'napi',
                'id': pool_id
            },
            'to': {
                'collection': 'comp_unit',
                'provider': 'globomap',
                'id': member['equipment']['name']
            },
            'content': {
                'id': member['id'],
                'name': member['identifier'],
                'properties': {
                    'ip': ip_formated,
                    'priority': member['priority'],
                    'weight': member['weight'],
                    'limit': member['limit'],
                    'port_real': member['port_real']
                }
            }
        }

        return data

    def comp_unit(self, compunit):
        """Prepare dict of compunit to send"""

        self._validate(compunit)
        data = {
            'collection': 'comp_unit',
            'content': {
                'id': compunit['name'],
                'name': compunit['name']
            }
        }

        return data
