#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
addr = re.compile(r'^addr+:([a-z]|_)*$')
addr_street = re.compile(r'^addr:street')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
fixme = re.compile(r'fixme', re.IGNORECASE)
street_box = re.compile(r'P\.O\. Box')
post_re = re.compile(r' |-')

mapping = { "St.": "Street",
           "St,": "Street",
            "Ave": "Avenue",
           "Rd": "Road",
            "Rd.": "Road"
            }

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def update_name(name, mapping):
    for key in mapping.keys():
        if key in name:
            name = name.replace(key, mapping[key])
    return name

def shape_created(node, k, i):
    if not "created" in node:
        node['created'] = {}
    node['created'][k] = i.get(k)
    

def shape_pos(node, k, i):
    if not "pos" in node:
        node['pos'] = [None] * 2
    if k == "lat":
        node['pos'][0] = float(i.get(k))
    else:
        node['pos'][1] = float(i.get(k))
        
def shape_nd(node, k, i):
    if not "node_refs" in node:
        node['node_refs'] = []
    node['node_refs'].append(i.get(k))
    
def shape_tag(node, i):
	k = i.attrib['k']
	v = i.attrib['v']
	if fixme.search(k):
		pass
	elif problemchars.search(k):
		pass
	elif k == "addr:state" or k == "addr:suburb":
		pass
	elif k == "addr:city":
		if not "address" in node:
			node['address'] = {}
		node['address']['city'] = 'Riyadh'
	elif k == "addr:country":
		if not "address" in node:
			node['address'] = {}
		node['address']['country'] = 'SA'
	elif k == "addr:postcode":
		if not "address" in node:
			node['address'] = {}
		node['address']['postcode'] = post_re.split(v)[0]
	elif addr.search(k):
		if addr_street.search(k) and street_type_re.search(v):
			if street_box.search(v):
				pass
			else:
				name = update_name(v, mapping)
				if not "address" in node:
					node['address'] = {}
				node['address'][k[5:]] = name
	elif lower_colon.search(i.attrib['k']):
		node[i.attrib['k']] = i.attrib['v']
    #pprint.pprint(node)

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way":
        if element.tag == "node":
            node['type'] = "node"
            for i in element.iter():
                if i.tag == "tag":
                    shape_tag(node, i)
                else:
                    for k in i.keys():
                        #Handling Created
                        if k in CREATED:
                            shape_created(node, k, i)
                        #Handling Position
                        elif k == "lat" or k == "lon":
                            shape_pos(node, k, i)
                        else:
                            node[k] = i.get(k)
        elif element.tag == "way":
            node['type'] = "way"
            for i in element.iter():
                if i.tag == "tag":
                    shape_tag(node, i)
                else:
                   for k in i.keys():
                       #Handling Created
                        if k in CREATED:
                            shape_created(node, k, i)
                        elif k == "ref":
                            shape_nd(node, k, i)
                        
                        else:
                            node[k] = i.get(k)
            
        #pprint.pprint(node)    
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "E:\\Riyadh\\Riyadh.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('E:\\Riyadh\\riyadh_saudi-arabia.osm', True)
    #pprint.pprint(data)
    

if __name__ == "__main__":
    test()
