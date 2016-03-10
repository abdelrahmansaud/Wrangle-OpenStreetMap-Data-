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
addr_country = re.compile(r'^addr:country')

def key_type(element, keys):
    if element.tag == "tag":
		k = element.attrib['k']
		v = element.attrib['v']
		if addr_country.search(k):
			keys[v] += 1
       
    return keys

def process_map(filename):
    keys = defaultdict(int)
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

def file_out(keys):
	with codecs.open('E:\\Riyadh\\country.json', "w") as fo:
			fo.write(json.dumps(keys, indent=2)+"\n")


if __name__ == "__main__":
    keys = process_map('E:\\Riyadh\\riyadh_saudi-arabia.osm')
    file_out(keys)