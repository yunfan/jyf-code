#!/usr/bin/env python2.5
# -*- coding:utf-8 -*-
# File: app.py
# Date: 2010-08-10
# Author: jyf<jyf1987@gmail.com>
# Comment:  

import time, os, web, setting
from docutils.core import publish_string

urls = (
        '/ws/doc/(.*)', 'rstRender',
)
application=web.application(urls,globals()).wsgifunc()

class rstRender:
    def GET(self, path):
        list_dir = lambda p: '<br/>'.join(map(lambda name: '''<a href="%(name)s">%(name)s</a>''' % {'name': name}, os.listdir(p)))

        fullpath = '%s%s' % ( setting.DOC_BASE_PATH, path)
        if os.path.isdir(fullpath):
            print 'Index: %s' % fullpath
            return list_dir(fullpath)          ## there's a leak here, eg, /home/jyf/../../
        elif not fullpath.endswith(".rst"):
            return reError(403, "require rst filetype")

        ## now process the target filetype
        if not os.path.exists(fullpath):
            return reError(404, "file: %s not exists" % path)
        else:
            print 'Fetch: %s' % fullpath
            fp = open(fullpath, 'rb')
            raw = fp.read()             ## large file will cause problem here
            fp.close()
            dst = publish_string(raw, writer_name='html4css1')      ## we can cache the content for next time use
            return dst

#####################################################
## 公用函数

def reError(code=0,desc=''):
    return '%d<br/>\n%s' % (code,desc)

web.wsgi.runwsgi = lambda func,addr = None: web.wsgi.runfcgi(func ,addr)

