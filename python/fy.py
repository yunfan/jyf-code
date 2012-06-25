#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: fy.py
# Date: 2010-04-25
# Author: jyf<jyf1987@gmail.com>
# Commnet: for wind
# License: WTFPL ( do what the fuck you want to do to it)

import sys,json,urllib


def translate(text, langPair="en|zh"):
	##print text,"\n",langPair
	query = {
		"v": "1.0",
		"q": text,
		}
	qstr = urllib.urlencode(query)
	serviceUrl = "http://ajax.googleapis.com/ajax/services/language/translate?%s&langpair=%s" % ( qstr, langPair )
	##print serviceUrl
	try:
		print >>sys.stdout, "正在请求远程服务...\n"
		re = urllib.urlopen(serviceUrl)
	except Exception,e:
		print >>sys.stderr,"打开远程服务地址时发生了一些情况，这里有附加的错误参考: %s" % repr(e.args)
		sys.exit(1)

	msg = re.read()

	##print msg
	res = json.loads(msg)
	
	if 200 == res["responseStatus"]:
		##print msg
		print >>sys.stdout, """原文: %s\n翻译: %s\n""" % ( text, res["responseData"]["translatedText"].encode("utf-8") )
	else:
		print >>sys.stderr, """老弟，服务器又返回错误了:\n%s\n""" % msg



def prepare():
	if 2 > len(sys.argv):
		print >>sys.stderr, "大佬，参数不够"
		sys.exit(0)
	text = sys.argv[1]
	langPair = "en|zh"
	for char in text:
		if  128 < ord(char):
			langPair = "zh|en"
			break
	translate(text, langPair)

if "__main__" == __name__:
	prepare()
