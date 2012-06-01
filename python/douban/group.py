#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback

from pyquery import PyQuery as pq

def discuss_page_fetch(url):
    try:
        cl = pq(url=url)
    except:
        traceback.print_exc()
        return []

    infos = cl("div#content div.article table.olt tr")
    if infos is None: return []
    infos.pop(0)

    tmp = [ rec.getchildren() for rec in infos]

    res = [ {   'title': rec[0].getchildren()[0].get('title'),
                'link': rec[0].getchildren()[0].get('href'),
                'author': (rec[1].getchildren()[0].get('href'), rec[1].getchildren()[0].text ),
                'reply_count': rec[2].text,
                'date': rec[3].text, } for rec in tmp ]

    return res

class Group(object):
    URL_BASE_TPL = '''http://www.douban.com/group/%s'''
    URL_DISCUSS_TPL = '''%s/discussion'''

    def __init__(self, url_code):
        self.url_code = url_code
        self.url_base = self.URL_BASE_TPL % self.url_code
        self.url_discuss = self.URL_DISCUSS_TPL % self.url_base

    def fetch(self, start=0, count=25):
        res = []
        tmp = discuss_page_fetch('%s?start=%d'%(self.url_discuss, start))
        if not tmp: return res

        while count > 0:
            try:
                rec = tmp.pop(0)
            except:
                start += 25
                tmp = discuss_page_fetch('%s?start=%d'%(self.url_discuss, start))
                if not tmp: return res
                continue

            res.append(rec)
            count -= 1

        return res

    def fetch_by_date(self, start_date=None, end_date=None):
        pass
