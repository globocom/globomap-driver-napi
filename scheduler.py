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
# !/usr/bin/env python
import logging
import sys

from apscheduler.schedulers.blocking import BlockingScheduler

from globomap_driver_napi.driver import Napi
from globomap_driver_napi.settings import SCHEDULER_FREQUENCY_EXEC

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='0-6', hour=SCHEDULER_FREQUENCY_EXEC)
def run_loader():
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s %(threadName)s %(levelname)s %(message)s',
        stream=sys.stdout
    )

    inst = Napi(connect_rabbitmq=False)
    inst.full_load()


if __name__ == '__main__':
    sched.start()
