#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: shared.py
# Date: 2009-11-25
# Author: jyf
# Comment: daemon for share service

import sys
from libcommon import daemon
import setting
import share


if __name__=='__main__':
    daemon.redirect_filelog('logdaemon.log')
    from flup.server import fcgi
    server=fcgi.WSGIServer(share.application,bindAddress=('0.0.0.0',setting.FCGIPORT))
    server.run()
