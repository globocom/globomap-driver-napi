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
