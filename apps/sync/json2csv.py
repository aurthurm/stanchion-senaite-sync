# -*- coding: utf-8 -*-
## Appreciation of this csv module goes to [vladikk](https://github.com/vladikk)

import logging
from itertools import chain
import json
import csv
from io import StringIO
import sys
from six import string_types

logger = logging.getLogger("json2csv")

def in_memory_json_to_csv(json, output_file_path):
    dicts = json_to_dicts(json)    
    with open(output_file_path, "w") as output_file:
        dicts_to_csv(dicts, output_file)

def json_to_csv(input_file_path, output_file_path):
    with open(input_file_path) as input_file:
        json = input_file.read()
    dicts = json_to_dicts(json)    
    with open(output_file_path, "w") as output_file:
        dicts_to_csv(dicts, output_file)

def json_to_dicts(json_str):
    try:
      objects = json.loads(json_str)
    except json.decoder.JSONDecodeError:
      objects = [json.loads(l) for l in json_str.split('\n') if l.strip()]

    return [dict(to_keyvalue_pairs(obj)) for obj in objects]

def to_keyvalue_pairs(source, ancestors=[], key_delimeter='_'):
    def is_sequence(arg):
        return (not isinstance(arg, string_types)) and (hasattr(arg, "__getitem__") or hasattr(arg, "__iter__"))

    def is_dict(arg):
        return isinstance(arg, dict)

    if is_dict(source):
        result = [to_keyvalue_pairs(source[key], ancestors + [key]) for key in source.keys()]
        return list(chain.from_iterable(result))
    elif is_sequence(source):
        result = [to_keyvalue_pairs(item, ancestors + [str(index)]) for (index, item) in enumerate(source)]
        return list(chain.from_iterable(result))
    else:
        return [(key_delimeter.join(ancestors), source)]

def dicts_to_csv(source, output_file):
    def build_row(dict_obj, keys):
        return [dict_obj.get(k, "") for k in keys]

    keys = sorted(set(chain.from_iterable([o.keys() for o in source])))
    rows = [build_row(d, keys) for d in source]

    cw = csv.writer(output_file)
    cw.writerow(keys)
    for row in rows:
        cw.writerow([c if isinstance(c, string_types) else c for c in row])

def write_csv(headers, rows, file):
    cw = csv.writer(file)
    cw.writerow(headers)
    for row in rows:
        cw.writerow([c.encode('utf-8') if isinstance(c, str) or isinstance(c, unicode) else c for c in row])