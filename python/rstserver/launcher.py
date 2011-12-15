#!/usr/bin/env python2.5
# -*- coding: UTF-8 -*-
# File: launcher.py
# Date: 2010-08-10
# Author: jyf<jyf1987@gmail.com>
# Deps: fcgi

import time, setting, app

now = lambda: time.strftime("%Y-%m-%d %H:%M:%S")

if __name__=='__main__':
    from flup.server import fcgi
    server=fcgi.WSGIServer(app.application,bindAddress=('0.0.0.0',setting.FCGIPORT))
    server.run()
