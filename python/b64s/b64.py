#!/usr/bin/env python2.5
# -*- coding:UTF-8 -*-
import random

cs = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def mix(s):
    l = len(s)-1
    r = ''
    while l >= 0:
        idx = random.randint(0,l)
        r = r + s[idx]
        s = s[:idx] + s[idx+1:]
        l = l -1

    #r = r + s
    return r

cs = mix(mix(cs))

def encode(s):
    max = len(s)
    r = ''
    for i in range(0,max,3):
        r = r + a324(s[i:i+3],cs)
    return r

def a324(s,cs):
    if len(s) > 3:
        return False
    if 1 == len(s):
        c1 = ord(s)
        c2 = c3 = 0
    elif 2 == len(s):
        c1 = ord(s[0])
        c2 = ord(s[1])
        c3 = 0
    else:
        c1 = ord(s[0]) 
        c2 = ord(s[1]) 
        c3 = ord(s[2])
    
    ct = c1*256**2 + c2*256 + c3
    #print "count = %d" % (ct)
    r1 = cs[ct / (64**3)]
    ct = ct % (64**3)
    r2 = cs[ct / (64**2)]
    ct = ct % (64**2)
    r3 = cs[ct / (64)]
    r4 = cs[ct % 64]
    if cs[0] == r3:
        r3 = '='
    if cs[0] == r4:
        r4 = '='

    return r1+r2+r3+r4


def decode(s):
    #cs = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    max = len(s)
    if (max % 4) != 0:
        return False
    r = ''
    for i in range(0,max,4):
        r = r + a423(s[i:i+4],cs)
    return r

def a423(s,cs):
    if len(s) != 4:
        return False
    c1 = cs.index(s[0])
    c2 = cs.index(s[1])
    try:
        c3 = cs.index(s[2])
    except:
        c3 = 0
    try:
        c4 = cs.index(s[3])
    except:
        c4 = 0
    ct = c1*64**3 + c2*64**2 + c3*64 + c4
    #print "count = %d" % (ct)
    r1 = ct / 256**2
    #print r1,ct
    ct = ct % (256**2)
    r2 = ct / 256
    #print r2,ct
    r3 = ct % 256
    #print r3,ct
    
    return chr(r1)+chr(r2)+chr(r3) 


if '__main__' == __name__:
    
    test = 'abc123中文@'
    result = encode(test)
    print "charset = [ %s ]" % (cs)
    print "encode result is : %s " % (result)
    original = decode(result)
    print "decode result is : %s " % (original)

