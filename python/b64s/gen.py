#!/usr/bin/env python2.5
# -*- coding: UTF-8 -*-
import random

cs = "23456789abcdefghijkmnpqrstuvwxyzABCDEFGHIJKMNPQRSTUVWXYZ"

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

def tun2(dec,xx):
    nr = 6
    #xx = 'ZYXWVUTSRQPNMLKJIHGFEDCBA98765432zyxwvutsrqpnmkjihgfedcba'
    max = len(xx)
    #print max
    r = ''
    while dec >= max:
        n = dec % max
        dec = dec / max
        #print n,dec
        r = r + xx[n]
    #print dec
    r = r + xx[dec]
    if len(r) < nr:
        r = r + xx[0]*(nr-len(r))   # 补全位数
    return r[::-1]


def tundec(s,xx):
    #xx = 'ZYXWVUTSRQPNMLKJIHGFEDCBA98765432zyxwvutsrqpnmkjihgfedcba'
    max = len(xx)
    dec = 0
    for i in range(len(s)):
        dec = dec + max**(len(s)-i-1)*xx.index(s[i])
    return dec
cs1 = mix(cs)
cs2 = mix(cs1)
cs3 = mix(cs2)

print cs,len(cs)
print cs1,len(cs1)
print cs2,len(cs2)
print cs3,len(cs3)

#b = random.randint(1,56**6)
b = 13612345678L
print b

print tun2(b,cs),tun2(b+1,cs)
print tun2(b,cs1),tun2(b+1,cs1)
print tun2(b,cs2),tun2(b+1,cs2)
print tun2(b,cs3),tun2(b+1,cs3)

