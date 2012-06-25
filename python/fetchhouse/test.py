#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq

trans = lambda x: (type(x) in (str, unicode)) and (( (type(x) == unicode) and x.encode('utf-8') ) or x) or x
filter = lambda x: dict(map(lambda k: (k.encode('utf-8'), trans(x[k])), x))

init_url = "http://bj.58.com/hongmiao/hezu/pn42/"


def info(idx, node):
    print "\n",idx
    tds = node.findall("td")
    rec = {}
    rec["price"] = int(tds[0].find("b").text)
    rec["type"] = tds[1].text
    rec["pubdate"] = tds[3].text
    links = tds[2].findall("a")
    rec["title"] = links[0].text
    ##print rec["title"].encode("utf-8")
    rec["url"] = links[0].get("href")
    if len(links) > 2:
        rec["area"] = links[2].text
    else:
        spans = map(lambda h: h.text, tds[2].findall("span"))
        rec["area"] = " ".join(spans[:-1])
        

    rec = filter(rec)

    print '{"title": "%(title)s", "type": "%(type)s", "price": "%(price)d", "area": "%(area)s"}' % rec

d = pq(url=init_url)
raw = d(r'#infolist tr')
raw.each(info)

links = d("div.pager a")
for  rec in links:
    url = rec.get("href")
    if url.startswith("http://"):
        
