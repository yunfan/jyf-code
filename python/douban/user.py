#!/usr/bin/env python
# -*- coding: utf-8 -*-

class User(object):
    def __init__(self, nick, uid=None, url_code=None):
        self.nick = nick
        self.uid = uid
        self.url_code = url_code
