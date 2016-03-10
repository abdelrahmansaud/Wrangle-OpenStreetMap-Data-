#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import codecs
import json
import pprint

def count_tags(filename):
        
        tags = {}
        for event, elem in ET.iterparse(filename):
            if elem.tag in tags:
                tags[elem.tag] = tags[elem.tag] + 1
            else:
                tags[elem.tag] = 1
        return tags

def file_out(tags):
	with codecs.open('E:\\Riyadh\\tags.json', "w") as fo:
			fo.write(json.dumps(tags, indent=2)+"\n")


if __name__ == "__main__":
    tags = count_tags('E:\\Riyadh\\riyadh_saudi-arabia.osm')
    file_out(tags)