#!/usr/bin/env python
import json
import logging

import pika

from .networkapi import NetworkAPI
from .settings import NETWORKAPI_RMQ_HOST
from .settings import NETWORKAPI_RMQ_PASSWORD
from .settings import NETWORKAPI_RMQ_PORT
from .settings import NETWORKAPI_RMQ_USER
from .settings import NETWORKAPI_RMQ_VIRTUAL_HOST


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

    def _map(self):

        map_func = {
            'ServerPool': self.pool,
            'VipRequest': self.vip,
        }
        return map_func

    def updates(self, number_messages=1):

        messages = []
        while True:
            try:
                message = self.get_message()
            except StopIteration:
                if messages:
                    yield messages
                break
            else:
                messages.append(message)
                if len(messages) == number_messages:
                    yield messages
                    messages = []

    def get_message(self):

        message = self._consumer().next()
        if isinstance(message, dict):
            func = self._map().get(message.get('kind'))
            if func:
                self.log.debug('Treating message {}'.format(message))
                # Message must be treat
                data = func(message['data']['id_object'])
                return data
            else:
                self.log.debug('Discarding message {}'.format(message))

    def pool(self, id_object):

        napi = NetworkAPI()
        pool = napi.get_pool(id_object)
        data = {
            'id': pool['id'],
            'name': pool['identifier'],
            'properties': {
                'default_port': pool['default_port'],
                'servicedownaction': pool['servicedownaction']['name'],
                'lb_method': pool['lb_method'],
                'default_limit': pool['default_limit'],
                'pool_created': pool['pool_created']
            }
        }
        return data

    def vip(self, id_object):
        napi = NetworkAPI()
        vip = napi.get_vip(id_object)
        data = {
            'id': vip['id'],
            'name': vip['identifier'],
            'properties': {
                'napi_created': vip['created'],
                'napi_ipv4': vip['ipv4'],
                'napi_ipv6': vip['ipv6'],
                'napi_environmentvip': vip['environmentvip'],
            }
        }
        return data

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
