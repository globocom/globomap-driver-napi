#!/usr/bin/env python
import json
import logging

import pika

from .data_spec import DataSpec
from .networkapi import NetworkAPI
from .settings import NETWORKAPI_RMQ_HOST
from .settings import NETWORKAPI_RMQ_PASSWORD
from .settings import NETWORKAPI_RMQ_PORT
from .settings import NETWORKAPI_RMQ_USER
from .settings import NETWORKAPI_RMQ_VIRTUAL_HOST

ACTIONS = {
    'Alterar': 'UPDATE',
    'Cadastrar': 'CREATE',
    'Remover': 'DELETE'
}


class Napi(object):

    log = logging.getLogger(__name__)

    def __init__(self):

        credentials = pika.PlainCredentials(
            NETWORKAPI_RMQ_USER, NETWORKAPI_RMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=NETWORKAPI_RMQ_HOST, port=NETWORKAPI_RMQ_PORT,
            virtual_host=NETWORKAPI_RMQ_VIRTUAL_HOST, credentials=credentials)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        self.msg_rest = []

    def _map(self):
        map_func = {
            'VipRequest': [
                {
                    'name': 'vip',
                    'func': self.vip,
                    'data_spec': DataSpec.vip,
                    'provider': 'napi'
                }
            ],
            'VipRequestPortPool': [
                {
                    'name': 'port',
                    'func': self.port,
                    'data_spec': DataSpec.port,
                    'provider': 'napi'
                }
            ],
            'ServerPool': [
                {
                    'name': 'pool',
                    'func': self.pool,
                    'data_spec': DataSpec.pool,
                    'provider': 'napi'
                }
            ],
            'ServerPoolMember': [
                {
                    'name': 'pool_comp_unit',
                    'func': self.pool_comp_unit,
                    'data_spec': DataSpec.pool_comp_unit,
                    'provider': 'napi'
                },
                {
                    'name': 'comp_unit',
                    'func': self.comp_unit,
                    'data_spec': DataSpec.comp_unit,
                    'provider': 'globomap'
                }
            ]
        }
        return map_func

    def _get_messages(self):
        message = self._consumer().next()

        if isinstance(message, dict):

            funcs = self._map().get(message.get('kind'))
            if funcs:
                self.log.debug('Treating message %s', message)
                msgs = []
                for func in funcs:
                    msgs.append(self._get_msg(func, message))
                return msgs
            else:
                self.log.debug('Discarding message %s', message)
                return self._get_messages()

    def _get_msg(self, kind, message):

        func = kind.get('func')
        name = kind.get('name')
        provider = kind.get('provider')

        action = ACTIONS.get(message.get('action'))
        id_object = message.get('data').get('id_object')

        update = {
            'action': action,
            'element': {
                'collection': name
            }
        }

        if action != 'DELETE':
            data = func(id_object)
            if data is not None:
                data['content']['timestamp'] = message.get('timestamp')
                data['content']['provider'] = provider
                update['element'].update(data)
        else:
            update['element']['content'] = {
                'id': id_object,
                'provider': provider
            }
        return update

    def _consumer(self):

        while True:
            method_frame, _, body = self.channel.basic_get('eventlog')
            if method_frame:
                self.channel.basic_ack(method_frame.delivery_tag)
                body = json.loads(body)
                yield body
            else:
                self.channel.close()
                self.connection.close()
                break

    def updates(self):
        """Return list of updates"""
        return self._updates().next()

    def _updates(self, number_messages=1):
        messages = []
        while True:
            try:
                if not self.msg_rest:
                    msgs = self._get_messages()
                    self.msg_rest = msgs
            except StopIteration:
                if messages:
                    yield messages
                raise StopIteration
            else:
                while True:
                    msg = self.msg_rest.pop(0)
                    messages.append(msg)
                    if len(messages) == number_messages:
                        yield messages
                        messages = []

    def vip(self, id_object):
        napi = NetworkAPI()
        vip = napi.get_vip(id_object)
        data = DataSpec().vip(vip)

        return data

    def pool(self, id_object):

        napi = NetworkAPI()
        pool = napi.get_pool(id_object)
        data = DataSpec().pool(pool)

        return data

    def port(self, id_object):

        napi = NetworkAPI()
        vip = napi.get_vip_by_portpool_id(id_object)
        data = None
        for port in vip['ports']:
            for pool in port['pools']:
                if pool['id'] == id_object:
                    pool['port'] = port['port']
                    data = DataSpec().port(pool, port['id'])
        if data is None:
            return False

        return data

    def comp_unit(self, id_object):

        napi = NetworkAPI()
        pool = napi.get_pool_by_member_id(id_object)

        data = DataSpec().pool(pool)
        if data is None:
            return False

        for member in pool['server_pool_members']:
            if member['id'] == id_object:
                eqpt = member['equipment']
                data = DataSpec().comp_unit(eqpt)

        return data

    def pool_comp_unit(self, id_object):
        napi = NetworkAPI()
        pool = napi.get_pool_by_member_id(id_object)

        data = DataSpec().pool(pool)
        if data is None:
            return False

        for member in pool['server_pool_members']:
            if member['id'] == id_object:
                data = DataSpec().pool_comp_unit(member, pool['id'])

        return data
