#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: model.py
# Date: 2010-08-18
# Author: jyf<jyf1987@gmail.com>

example_rec = {"price": 0, "class": "户型", "area": 0, "type": "装修", "loc": "小区", "addr": "具体地址", "widget": "配置", "desc": "说明", "mobile": "手机"}

##fp = open("data.json", "wb")

import pymongo
conn = pymongo.Connection()
tbl = conn['house']['info3']

def addrec(rec):
    ##info = """{ "price": %(price)d, "class": "%(class)s", "area": %(area)d, "type": "%(type)s", "loc": "%(loc)s", "addr": "%(addr)s", "widget": "%(widget)s", "desc": "%(desc)s", "mobile": "%(mobile)s", "page": "%(page)s" }\n""" % rec
    ##fp.write(info)
    tbl.insert(rec)

