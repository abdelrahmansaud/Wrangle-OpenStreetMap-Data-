#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import re
import codecs
import json
import pprint
from collections import defaultdict

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        k = element.attrib['k']
        if problemchars.search(k):
            keys['problemchars'] += 1
        elif lower_colon.search(k):
            keys['lower_colon'] += 1
        elif lower.search(k):
            keys['lower'] += 1
        else:
			keys['others'][k] += 1
			keys['other'] += 1
        pass
       
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0, "others": defaultdict(int)}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

def file_out(keys):
	with codecs.open('E:\\Riyadh\\tag_types.json', "w") as fo:
			fo.write(json.dumps(keys, indent=2)+"\n")


if __name__ == "__main__":
    keys = process_map('E:\\Riyadh\\riyadh_saudi-arabia.osm')
    file_out(keys)