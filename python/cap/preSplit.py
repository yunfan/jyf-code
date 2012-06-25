#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: preSplit.py
# Date: 2010-01-27
# Author: jyf<jyf1987@gmail.com>
# Comment: 主席说 for-ever.us的验证码不好识别,所以写段代码先把图片预处理一下
#

import Image,sys

def main(fn):
    im = Image.open(fn)
    im = replace(im, (128,128,255), (0,0,0))        ## 去掉干扰纹 颜色提取 感谢 唐雯,下同
    im = replace(im, (227,218,237), (0,0,0))        ## 去掉背景色
    im = replace(im, (128,191,255), (0,0,0))        ## 去掉格纹
    im = replace2(im, (0,0,0), (255,255,255))       ## 统一字母颜色
    pre_fn = "pre_%s" % fn
    im.save(pre_fn)

def replace(im,colo1,colo2):
    """replace the point's color to colo2 which match colo1"""
    try:
        (x0,y0,x1,y1) = im.getbbox()
    except:
        print "you need to give me a image handle"
    for x in range(x0,x1):
        for y in range(y0,y1):
            r,g,b = im.getpixel((x,y))
            if r == colo1[0] and g == colo1[1] and b == colo1[2]:
                im.putpixel((x,y),colo2)

    return im

def replace2(im,colo1,colo2):
    """replace the point's color to colo2 which dismatch colo1"""
    try:
        (x0,y0,x1,y1) = im.getbbox()
    except:
        print "you need to give me a image handle"
    for x in range(x0,x1):
        for y in range(y0,y1):
            r,g,b = im.getpixel((x,y))
            if r != colo1[0] and g != colo1[1] and b != colo1[2]:
                im.putpixel((x,y),colo2)

    return im
    


if '__main__' == __name__:
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            fn = sys.argv[i]
            print "start process %s" % fn
            main(fn)
            print "process %s ok\n" % fn
    else:
        print """usage: python %s 1.png 2.png etc""" % sys.argv[0]
