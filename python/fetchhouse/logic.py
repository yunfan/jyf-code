#!/usr/bin/env python
# -*- coding: utf-8 -*
# File: logic.py
# Date: 2010-08-17
# Author: jyf<jyf1987@gmail.com>

"""becareful sometims it will took us coredump"""
from pyquery import PyQuery as pq
import re, Queue, threading, time
import model

trans = lambda x: (type(x) in (str, unicode)) and (( (type(x) == unicode) and x.encode('utf-8') ) or x) or x
filter = lambda x: dict(map(lambda k: (k.encode('utf-8'), trans(x[k])), x))
date_before = lambda x,y: ( x[0] == y[0] ) and ( x[1] < y[1] ) or ( x[0] < y[0] )
num_get = re.compile(r'[0-9]+', re.DOTALL)
tmp_get = re.compile(r'"([^"]+)"', re.DOTALL)

class PageWorker(threading.Thread):
    """page processer"""
    def run(self):
        while True:
            job = jobs.get()
            if not job:
                break 
            else:
                pageurl = job
                self.process(pageurl)

        print "%s done!" % self.getName()

    def process(self, url):
        rec = {"price": 0, "class": "户型", "area": 0, "type": "装修", "loc": "小区", "addr": "具体地址", "widget": "配置", "desc": "说明", "mobile": "手机"}
        print "InfoProcess: %s" % url
        try:
            o = pq(url=url)
        except:
            return
        infos = o("div.warp ul.info li")
        
        rec["mobile"] = trans(o("div.warp div.user span.phone").text())
        rec["page"] = url
        prices = trans(infos.eq(0)("em").text())
        try:
            rec["price"] = int(prices)
        except:
            rec["price"] = 0
        
        rec["class"] = trans(infos.eq(1).remove("i").text())

        areas = trans(infos.eq(2).remove("i").text())
        #print type(areas)
        areas = num_get.findall(areas)[0]
        try:
            rec["area"] = int(areas)
        except:
            rec["area"] = 0
        
        rec["type"] = trans(infos.eq(4).remove("i").text())
        rec["loc"] = trans(infos.eq(6).remove("i").text())
        rec["addr"] = trans(infos.eq(7).remove("i").text())

        widgets = trans(infos.eq(8).remove("i").text())
        try:
            rec["widget"] = tmp_get.findall(widgets)[0]
        except:
            rec["widget"] = ""

        rec["desc"] = trans(o("div.conleft p").text()).replace("\n","")
        stores.put(rec)

class StoreWorker(threading.Thread):
    def run(self):
        while True:
            rec = stores.get()
            if not rec:
                break
            else:
                self.addRec(rec)

        print "%s done!" % self.getName()

    def addRec(self, rec):
        model.addrec(rec)

def main(start_page, endDate):
    global jobs, stores, pager
    jobs = Queue.Queue()
    stores = Queue.Queue()
    pager = {}
    worker_ct = 10
    ##endDate = ( 7, 1 )

    for i in range(worker_ct):
        th = PageWorker()
        th.setDaemon(True)
        th.start()

    store_daemon = StoreWorker()
    store_daemon.setDaemon(True)
    store_daemon.start()

    def ListProcess(init_url):
        print "init url: %s" % init_url
        url = init_url
        if not url.startswith("http://"):
            raise Exception("url is not legal")

        host = "/".join(url.split("/")[:3])

        max = 0
        while True:
            max += 1
            if max > 100:
                break
            stopSig = False
            print "ListProcess: %s" % url
            try:
                d = pq(url=url)
            except:
                continue
            items = d(r'#infolist tr')
            print items
            nextpage = trans(d(r'div.pager strong').next().attr.href)
            if not nextpage.startswith("http://"):
                nextpage = "%s%s" % ( host, nextpage)
            url = nextpage
            print "\nNextPage = %s\n" % url

            for rec in items:
                tds = pq(rec)("td")
                price = trans(tds.eq(0)("b").text())
                try:
                    price = int(price)
                except:
                    price = 0
                if (price == 0) or (price >900):
                    continue
                infourl = trans(tds.eq(2)("a").eq(0).attr.href)
                if not infourl.startswith("http://"):
                    infourl = "%s%s" % ( host, infourl)

                pubdate = trans(tds.eq(3).text())
                if len(pubdate.split('-')) > 1:
                    pub = map(int, pubdate.split('-'))
                    stopSig = date_before(endDate, pub)
                if stopSig:
                    break
                else:
                    jobs.put(infourl)

            if stopSig:
                break

        print "listpage achive endDate"
    
    ##init_url = "http://bj.58.com/hongmiao/hezu/pn1"
    init_url = start_page
    ListProcess(init_url)

    for i in range(worker_ct):
        jobs.put(None)
    
    time.sleep(2)
    ##model.fp.close()
    print "ok, all job done"

if '__main__' == __name__:
    main()
