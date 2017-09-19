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
from pika.exceptions import ConnectionClosed

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

    logger = logging.getLogger(__name__)

    def __init__(self):

        self._connect_rabbit()

    def _connect_rabbit(self):
        self.rabbitmq = RabbitMQClient(
            host=NETWORKAPI_RMQ_HOST,
            port=NETWORKAPI_RMQ_PORT,
            user=NETWORKAPI_RMQ_USER,
            password=NETWORKAPI_RMQ_PASSWORD,
            vhost=NETWORKAPI_RMQ_VIRTUAL_HOST,
            queue_name=NETWORKAPI_RMQ_QUEUE
        )

    def _create_updates(self, raw_msg):
        """
        Creates update documents/edges documents for some events for NetworkAPI.
        This events are filtered by config in settings.
        """

        if isinstance(raw_msg, dict):
            # MAP_FUNC have mapping of messages types.
            # Messages not mapped are discarted
            funcs = MAP_FUNC.get(raw_msg.get('kind'))
            if funcs:
                messages_processed = []
                for func in funcs:
                    msgs = self._treat_message_by_func(func, raw_msg)
                    if msgs:
                        messages_processed += msgs
                return messages_processed

        self.logger.debug('Discarding message %s.', raw_msg)

        return []

    def _treat_message_by_func(self, func, message):

        self.logger.debug(
            'Processing message %s with function %s' % (message, func))
        try:
            msgs = self._processing_message(func, message)
            if not msgs:
                self.logger.debug(
                    'Message %s with function %s was not processed' %
                    (message, func))
            else:
                self.logger.debug(
                    'Message %s with function %s was processed' %
                    (message, func))
            return msgs
        except Exception as err:
            self.logger.error(
                'Message %s with problem. Error: %s.' % (message, err))

    def _processing_message(self, func, message):

        package = func.get('package')
        func_class = func.get('class')
        method = func.get('method')

        class_type = getattr(importlib.import_module(package), func_class)
        data = getattr(class_type(), method)(message)

        return data

    def process_updates(self, callback):
        """
        Reads and processes messages from the NetworkAPI event bus until
        there's no message left in the target queue. Only acks message if
        processed successfully by the callback.
        """
        while True:
            delivery_tag = None
            try:
                raw_msg, delivery_tag = self.rabbitmq.get_message()
                if raw_msg:
                    updates = self._create_updates(raw_msg)
                    for update in updates:
                        callback(update)

                    self.rabbitmq.ack_message(delivery_tag)
                else:
                    return
            except ConnectionClosed:
                self.logger.error('Error connecting to RabbitMQ, reconnecting')
                self._connect_rabbit()
            except:
                self.rabbitmq.nack_message(delivery_tag)
                raise
