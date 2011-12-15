# -*- coding: utf-8 -*-
import spaces_pb2
from libcommon import json

si = spaces_pb2.SpaceInfo()

si.id = 1024
si.name = "his_name"
si.description = "his_desc"

def typestr(obj):
    raw = repr(type(obj))
    q1 = raw.find("'")
    q2 = raw.find("'",q1+1)
    return raw[1:q1-1],raw[q1+1:q2]

def proto2hash(pbobj,filter=True):
    """filter 过滤空值"""
    t,s = typestr(pbobj)
    if ('class' == t):
        print 'class'
        res = {}
        for raw_item in dir(pbobj):
            if "_value_" in raw_item:
                val = getattr(pbobj,raw_item)
                t,s = typestr(val)
                if s in ['bool','int','long','float','complex','str','unicode']:
                    item = raw_item[7:]
                    if not filter:
                        res[item] = val
                    elif val:
                        res[item] = val

                elif ( s in ['list','tuple','dict'] ) or 'class' == t:
                    if not filter: 
                        res[item] = proto2hash(val)
                    elif val:
                        res[item] = proto2hash(val)
        return res

    elif s in ['list','tuple']:
        print 'list_tuple'
        res = []
        for item in pbobj:
                t,s = typestr(item)
                if s in ['bool','int','long','float','complex']:
                    if not filter:
                        res.append(item)
                    elif item:
                        res.append(item)
                
                elif ( s in ['list','tuple','dict'] ) or 'class' == t:
                    if not fileter:
                        res.append(proto2hash(val))
                    elif item:
                        res.append(proto2hash(val))
                        
        return res    
           
    elif 'dict' == s:
        print 'dict'
        res = {}
        for item in pbobj.keys():
                print item
                val = pbobj[item]
                t,s = typestr(val)
                print t,s
                if s in ['bool','int','long','float','complex']:
                    if not filter:
                        res[item] = val
                    elif val:
                        res[item] = val

                elif ( s in ['list','tuple','dict'] ) or ( 'class' == t ):
                    if not filter:
                        res[item] = proto2hash(val)
                    elif val:
                        res[item] = proto2hash(val)
        return res    


print json.write(proto2hash({'space1':si,'space2':si,'space3':si}))
