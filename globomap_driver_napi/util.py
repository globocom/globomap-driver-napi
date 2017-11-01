import re


def valid_comp_unit_id(compunit):
    regex = re.search(
        '([0-9a-z]+)-([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$)',
        compunit
    )

    compunit_id = compunit if regex is None else regex.group(2)

    return compunit_id


def clear(collection, type, timestamp):
    data = {
        'action': 'CLEAR',
        'collection': collection,
        'type': type,
        'element': [[{'field': 'timestamp', 'value': timestamp, 'operator': '<'}]]
    }
    return data
