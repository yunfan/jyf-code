#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
# File: xmppio.py
# Date: 2010-04-20
# Author: jyf<jyf1987@gmail.com>

from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import bot


class XMPPHandler(webapp.RequestHandler):
    def get(self):
        return """<script>alert("hello,world");</script>"""

    def post(self):
        jid = self.request.get("from")
        body = self.request.get("body")

        req = {}
        req["from"] = {"full": jid, "node": jid.split("/")[0].split("@")[0], "domain": jid.split("/")[0].split("@")[1], "resource": jid.split("/")[1]}
        req["raw"] = body
        response = bot.main(req)
        xmpp.send_message(jid, response)

urls = [
    ('/_ah/xmpp/message/chat/', XMPPHandler)
]


app = webapp.WSGIApplication(urls , debug=True)
if __name__ == "__main__":
  run_wsgi_app(app)
