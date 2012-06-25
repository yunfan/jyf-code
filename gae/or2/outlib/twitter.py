#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-
# File: twitter.py
# Date: 2009-9-10
# Author: jyf1987

# Comment: Simple twitter client for GAE
"""不严谨,凑合用
No strict validate,so Be careful.
BTW: the lincense is:
@Do what you want to do to this code@
"""

from google.appengine.api import urlfetch
from urllib import urlencode,unquote
from binascii import b2a_base64 as b64
from django.utils import simplejson as json

def urlen(s):
    b = ['%'+'%X' % ord(d) for d in s]
    return ''.join(b)

class Twitter:
  def __init__(self, user, passwd, base_url="http://twitter.com/"):
    self.user = user
    self.passwd = passwd
    self.passstr = b64('%s:%s' % (self.user , self.passwd))
    self.passstr = self.passstr[:-1]   ## This is because the binascii.b2a_base64 will append an extra '\n' to the string
    self.url = base_url

  def update_status(self, status):
    url = self.url + 'statuses/update.json'
    payload = {'status':status.encode('utf-8'),'source':'GAE'}
    #payload = 'status=%s&source=%s' % (status , 'GAE')
    method = urlfetch.POST
    return self.Auth_client(url,payload,method)

  def get_public_timeline(self):
    url = self.url + 'statuses/public_timeline.json'
    return self.Auth_client(url)

  def get_friends_timeline(self):
    url = self.url + 'statuses/friends_timeline.json'
    return self.Auth_client(url)

  def get_replies(self):
    url = self.url + 'statuses/replies.json'
    return self.Auth_client(url)

  def Auth_client(self,url,payload='',method=urlfetch.GET,extra_headers={}):
    headers = {'Authorization':'Basic %s' % self.passstr}
    for k in extra_headers:
        headers[k] = extra_headers[k]
    payload_str = urlencode(payload)
    self.result = urlfetch.fetch(url , payload=payload_str , method=method, headers=headers)
    data = json.loads(self.result.content)
    return data
    
