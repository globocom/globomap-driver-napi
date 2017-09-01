#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from loader import Loader

if __name__ == '__main__':
    logging.basicConfig(
        filename='loader.log',
        level=logging.DEBUG,
        format='%(asctime)s %(threadName)s %(levelname)s %(message)s')

    inst_loader = Loader()

    for messages in inst_loader.vips():
        inst_loader.send(messages)

    for messages in inst_loader.pools():
        inst_loader.send(messages)

    for messages in inst_loader.environments():
        inst_loader.send(messages)

    for messages in inst_loader.vlans():
        inst_loader.send(messages)

    for messages in inst_loader.networksv4():
        inst_loader.send(messages)

    for messages in inst_loader.networksv6():
        inst_loader.send(messages)

    for messages in inst_loader.equipments():
        inst_loader.send(messages)
