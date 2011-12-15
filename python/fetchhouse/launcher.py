#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: launcher.py
# Date: 2010-08-18
# Author: jyf<jyf1987@gmail.com>
# Comment: this is job control script

"""i will give my thanks to 58.com, they provide the infomations"""

import logic

endDate = ( 8, 15)

##dstarea =  ('shuangjing', 'tuanjiehu', 'chaoyanggongyuan', 'hujialou', 'dongba', 'yaojiayuan', 'shuiduizi', 'tianshuiyuan', 'chaoqingbankuai', 'shifoying', 'shilibao', 'hongmiao'):
dstarea =  ('tuanjiehu', 'chaoyanggongyuan', 'hujialou', 'shuiduizi', 'tianshuiyuan', 'hongmiao')

for loc in dstarea:
    for cls in ('hezu', 'zufang'):
        url = """http://bj.58.com/%s/%s/pn1""" % ( loc, cls)
        logic.main(url, endDate)
