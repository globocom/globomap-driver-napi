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
                    try:
                        msg = self._treat_message(func, message)
                        if msg:
                            msgs.append(msg)
                        else:
                            self.log.debug(
                                'Message don\'t treated %s.', message)
                    except Exception as err:
                        self.log.error(
                            'Message with problem %s. Error: %s' % (message, err))
                if not msgs:
                    return self.next_message()
                return msgs
            else:
                self.log.debug('Discarding message %s', message)
                return self.next_message()

    def _treat_message(self, kind, message):

        package = kind.get('package')
        kind_class = kind.get('class')
        method = kind.get('method')

        class_type = getattr(importlib.import_module(package), kind_class)
        data = getattr(class_type(), method)(message)

        return data

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
                    if self.msg_rest:
                        msg = self.msg_rest.pop(0)
                        messages.append(msg)
                    if len(messages) == number_messages:
                        yield messages

                    if not self.msg_rest:
                        break
