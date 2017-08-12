#!/usr/bin/env python
import logging

from globomap_driver_napi.loader import Loader

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(threadName)s %(levelname)s %(message)s')

    inst_loader = Loader()

    for messages in inst_loader.vips():
        inst_loader.send(messages)

    for messages in inst_loader.pools():
        inst_loader.send(messages)
