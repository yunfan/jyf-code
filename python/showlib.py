#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys

def dump(dir,n=0):
    print "%s%s" % (" "*n , dir)
    for f in os.listdir(dir):
	tf = os.path.join(dir,f)
	if os.path.isfile(tf) and ".py" == f[-3:]:
	    print "%s%s" % (" "*n , tf)
	elif os.path.isdir(f):
	    dump(tf,n+2)

print "200\n\n"

for d in sys.path:
    if os.path.isdir(d):
	dump(d)
    else:
	print d
