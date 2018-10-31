"""
   Copyright 2018 Globo.com

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
from logging import config
from logging import getLogger
from time import sleep

from globomap_loader_api_client import auth
from globomap_loader_api_client.update import Update

from globomap_driver_napi import settings
from globomap_driver_napi.driver import Napi


LOGGER = getLogger(__name__)


def run():
    while True:
        inst = Napi()
        auth_inst = auth.Auth(
            api_url=settings.GLOBOMAP_LOADER_API_URL,
            username=settings.GLOBOMAP_LOADER_API_USERNAME,
            password=settings.GLOBOMAP_LOADER_API_PASSWORD
        )
        update = Update(auth=auth_inst, driver_name='napi')
        try:
            inst.process_updates(update.post)
        except Exception:
            LOGGER.exception('Error syncing updates from driver')
        finally:
            LOGGER.debug('No more updates found')
            LOGGER.debug('Sleeping for %ss' % 30)
            sleep(30)


if __name__ == '__main__':
    config.dictConfig(settings.LOGGING)
    run()
