#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
import re

try:
    import json
except ImportError:
    import simplejson as json

AT_PICKER = re.compile(r'''\s@([^ ",:]+)''', re.I | re.M | re.S | re.U)

def main():
    if len(sys.argv) != 2:
        print "fuckoff"
        sys.exit(1)
    name = sys.argv[1]
    fn = open('%s.json'%name, "r")

    info = {'forward': 0, 'ats': []}

    for l in fn.xreadlines():
        msg = json.loads(l)
        ##print msg['message']
        if msg['isforward'] is not None:
            info['forward'] += 1
        res = AT_PICKER.findall(l)
        if res:
            #print res
            info['ats'].extend(res)

    print '转发',info['forward']
    print '@过的'
    for name in set(info['ats']):
        print name

if '__main__' == __name__:
    main()
