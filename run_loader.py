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
