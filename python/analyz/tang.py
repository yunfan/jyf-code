#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
# File: 
# Date: 
# Author: jyf<jyf1987@gmail.com>
# Comment: 

src = "zh-tang300-utf8"

def main():
    fp = open(src, "rb")
    lines = fp.readlines()
    result = {}
    for line in lines:
        line = unicode(line, "utf8")
        if '\x1b' == line[0]:
            continue    ## 标题和作者介绍之类的
        for key in line:
            if key not in result:
                result[key] = 1
            else:
                result[key] += 1
    
    res = []
    for key in result:
        res.append((key.encode("utf-8"), result[key]))
    
    def my_cmp(x,y):
        return 0-cmp(x[1], y[1])

    res.sort(my_cmp)

    for v in res:
        print "%s\t%d" % ( v[0], v[1])

if '__main__' == __name__:
    main()
