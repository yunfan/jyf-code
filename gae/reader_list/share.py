#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: share.py
# Date: 2009-11-25
# Author: jyf
# Comment: share service

import web
from libcommon import dbutil
import setting

urls = {
    '/share/add' , 'addItem',
    '/share/show' , 'showItem'
}


application = web.application(urls,globals()).wsgifunc()
calllog=daemon.CallLog(setting.LOGTPL)

class addItem:
    @calllog
    def GET(self):
        """accept share items"""
        """http://jyf1987.3322.org/share/add?source=${source}&title=${title}&raw-url=${url}&shor-url=${short-url}&user=jyf"""
        req = web.input()
        req_key = req.keys()
        from_ip = web.ctx.env.get('REMOTE_ADDR' , 'noip')
        if 'source' not in req_key:
            return reError(1 , 'source not exists')
        else:
            source = req['source']

        if 'title' not in req_key:
            return reError(2 , 'title not exists')
        else:
            title = req['title']

        if 'raw-url' not in req_key:
            return reError(3 , 'raw-url not exists')
        else:
            raw_url = req['raw-url']
    
        if 'short-url' not in req_key:
            return reError(4 , 'short-url not exists')
        else:
            short_url = req['short-url']
    
        if 'user' not in req_key:
            user = 'user@%s' % from_ip
        else:
            user = req['user']
        
        dbutil.__init__(setting.DB_PARAMS)
        qd = {'source': source , 'title': title , 'raw_url': raw_url , 'short_url': short_url , 'add_user': user , 'from_ip': from_ip}
        sql = setting.ITEM_ADD % qd
        raw = dbutil.update(sql)
        return raw

class showItem:
    @calllog
    def GET(self):




#####################################################
## 公用函数

def reError(code=0,desc=''):
    return '%d\n%s' % (code,desc)
    #return '%d' % code
    #return '0'
