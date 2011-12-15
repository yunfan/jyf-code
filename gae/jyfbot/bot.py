#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: bot.py
# Date: 2010-04-20
# Author: jyf<jyf1987@gmail.com>

import re

class RPC:
    """RPC style processor"""
    def __init__(self,req,maps):
        self.maps = maps
        self.req = req
    
    def run(self):
        req = self.req
        try:
            for kv in self.maps:
                m = re.match(kv[0], req["raw"])
                if m:
                    req["argv"] = m.groups()
                    return kv[1](req)
            return "42!No match"
        except Exception,e:
            return repr(e.args)

def main(req):
    maps = (
        (r'^hi\s+(.*)', sayHello),
    )
    func = RPC(req,maps)
    return func.run()


def sayHello(req):
    import time
    now = lambda : time.strftime("%Y-%m-%d %H:%M:%S")
    return """[%s] Hi, %s, may name is not %s""" % ( now(), req["from"]["node"], req["argv"][0])
