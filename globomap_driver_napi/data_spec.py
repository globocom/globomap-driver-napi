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
            'id': vip['id'],
            'name': vip['name'],
            'provider': 'napi',
            'properties': [
                {'key': 'created', 'value': vip['created']},
                {'key': 'ip', 'value': ip_formated},
                {'key': 'environmentvip', 'value': envvip}
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
            'id': port['id'],
            'name': str(name),
            'provider': 'napi'
        }

        return data

    def pool(self, pool):
        """Prepare dict of Pool to send"""

        self._validate(pool)
        data = {
            'id': pool['id'],
            'name': pool['identifier'],
            'provider': 'napi',
            'properties': [
                {
                    'key': 'default_port',
                    'value': pool['default_port']
                },
                {
                    'key': 'environment',
                    'value': pool['environment']['name']
                },
                {
                    'key': 'servicedownaction',
                    'value': pool['servicedownaction']['name']},
                {
                    'key': 'healthcheck',
                    'value': pool['healthcheck']['healthcheck_type']
                },
                {
                    'key': 'lb_method',
                    'value': pool['lb_method']
                },
                {
                    'key': 'default_limit',
                    'value': pool['default_limit']
                },
                {
                    'key': 'pool_created',
                    'value': pool['pool_created']
                }
            ]
        }
        return data

    def pool_comp_unit(self, member, pool_id):
        """Prepare dict of Member to send."""

        self._validate(member)
        ip_formated = member['ip']['ip_formated'] \
            if member['ip'] else member['ipv6']['ip_formated']
        data = {
            'from': 'pool/napi_{}'.format(pool_id),
            'to': 'comp_unit/globomap_{}'.format(member['equipment']['name']),
            'id': member['id'],
            'name': member['identifier'],
            'provider': 'napi',
            'properties': [
                {'key': 'ip', 'value': ip_formated},
                {'key': 'priority', 'value': member['priority']},
                {'key': 'weight', 'value': member['weight']},
                {'key': 'limit', 'value': member['limit']},
                {'key': 'port_real', 'value': member['port_real']}
            ]
        }

        return data

    def comp_unit(self, compunit):
        """Prepare dict of compunit to send"""

        self._validate(compunit)
        data = {
            'id': compunit['name'],
            'name': compunit['name'],
            'provider': 'globomap'
        }

        return data
