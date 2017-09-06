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
import copy
import json
from operator import itemgetter


def open_json(json_file):
    with open(json_file) as data_file:
        data = json.load(data_file)
        return data


def dump_dict(received, expected):
    expected_data = json.dumps(expected, sort_keys=True)
    received_data = json.dumps(received, sort_keys=True)

    return received_data, expected_data


def as_json(data):
    return json.dumps(data)
