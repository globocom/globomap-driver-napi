#!/usr/bin/env python
import importlib
import json
import logging

import pika

from .data_spec import DataSpec
from .networkapi import NetworkAPI
from .rabbitmq import RabbitMQClient
from .settings import MAP_FUNC
from .settings import NETWORKAPI_RMQ_HOST
from .settings import NETWORKAPI_RMQ_PASSWORD
from .settings import NETWORKAPI_RMQ_PORT
from .settings import NETWORKAPI_RMQ_QUEUE
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

        self._connection()
        self.msg_rest = []

    def _connection(self):
        self.rabbitmq = RabbitMQClient(
            host=NETWORKAPI_RMQ_HOST,
            port=NETWORKAPI_RMQ_PORT,
            user=NETWORKAPI_RMQ_USER,
            password=NETWORKAPI_RMQ_PASSWORD,
            vhost=NETWORKAPI_RMQ_VIRTUAL_HOST,
            queue_name=NETWORKAPI_RMQ_QUEUE
        )

    def next_message(self):
        message = self.rabbitmq.get_message()
        if isinstance(message, dict):
            funcs = MAP_FUNC.get(message.get('kind'))
            if funcs:
                self.log.debug('Treating message %s', message)
                msgs = []
                for func in funcs:
                    msgs.append(self._treat_message(func, message))
                return msgs
            else:
                self.log.debug('Discarding message %s', message)
                return self.next_message()

    def _treat_message(self, kind, message):

        package = kind.get('package')
        kind_class = kind.get('class')
        method = kind.get('method')
        name = kind.get('name')
        provider = kind.get('provider')
        type_coll = kind.get('type')

        try:
            class_type = getattr(importlib.import_module(package), kind_class)
            if not hasattr(class_type, method) and \
                    not callable(getattr(class_type, method)):
                raise AttributeError(
                    'Kind {} does not implement the method {}'.format(
                        kind_class, method
                    )
                )
            self.log.debug("Kind '%s' loaded" % class_type)
        except AttributeError:
            self.log.error('Cannot load kind %s attribute not found'
                           % kind_class)
        except ImportError:
            self.log.error('Cannot load kind %s. Module not found %s'
                           % (kind_class, package))

        action = ACTIONS.get(message.get('action'))
        id_object = message.get('data').get('id_object')

        update = {
            'action': action,
            'collection': name,
            'type': type_coll,
            'element': {}
        }

        if action != 'DELETE':
            data = getattr(class_type(), method)(id_object)
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

    def updates(self, number_messages=1):
        """Return list of updates"""
        return self._get_update(number_messages).next()

    def _get_update(self, number_messages=1):
        messages = []
        while True:
            try:
                if not self.msg_rest:
                    self.msg_rest = self.next_message()
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
