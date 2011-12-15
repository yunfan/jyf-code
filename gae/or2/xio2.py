#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
# File: xio2.py
# Date: 2009-9-10
# Author: jyf1987
import web
from outlib.twitter import Twitter
import urllib
import setting
from google.appengine.api import xmpp
#to ensure the utf8 encoding environment
#import sys
#default_encoding = 'utf-8'
#if sys.getdefaultencoding() != default_encoding:
#	reload(sys)
#	sys.setdefaultencoding(default_encoding)


def urlencode(s):
    b = ['%'+'%X' % ord(d) for d in s]
    return ''.join(b)


class XMPPHandler():
    def GET(self):
	    req = web.input()
	    jid = req['jid']
	    user = xmpp.get_presence(jid)
	    if not user:
	        xmpp.send_invite(jid)
	    else:
	        return "user %s is online" % (jid)

    def POST(self):
        req = web.input()
        message = xmpp.Message(req)
        twclient = Twitter(setting.user,setting.pwd)
        #req["body"] = req["body"]
        message.reply("Debug:\nbody=%s" % repr(type(req['body'])))
        twmsg = "%s:"%(req['from'].split('/')[0]) + req["body"]
        #twmsg = 'f'*900
        if 140 < len(twmsg):
            message.reply("sorry,your msg's length is longer thant 140 bytes")
        else:
            res = twclient.update_status(twmsg)
            msg2 = """
msg has already sent,Its id is %(msgid)s
now we got %(sct)d status published
""" 
            x = {'msgid':res['id'] , 'sct':res['user']['statuses_count']}
            message.reply(msg2 % x)
            #message.reply(repr(res))


urls = (
	'/_ah/xmpp/message/chat/', XMPPHandler
	)

app = web.application(urls , globals())

if __name__ == "__main__":
  app.cgirun()
