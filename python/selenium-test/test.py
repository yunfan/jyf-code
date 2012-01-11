#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import urllib2
import traceback
from pprint import pprint as pp
import time

try:
    import json
except ImportError:
    import simplejson as json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


SINA_LOGIN_URL = 'http://weibo.com/login.php'
LOGIN_PATH = '/login.php'

def debug(msg):
    print msg
    pass

def init():
    fp = webdriver.FirefoxProfile()
    fp.add_extension(extension='firebug-1.9.0.xpi')
    fp.set_preference("extensions.firebug.currentVersion", "1.9.0")
    agent = webdriver.Firefox(firefox_profile=fp)
    return agent

def check_login_succ(agent):
    debug("checklogin")
    debug(agent.current_url)
    query_path = urllib2.urlparse.urlparse(agent.current_url)[2]
    return True if query_path != LOGIN_PATH else False

def check_nav_bar(agent):
    try:
        debug("checknavbar/scroll")
        agent.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        debug("checknavbar/findwpage")
        nav = agent.find_element_by_css_selector("div.W_pages")
    except NoSuchElementException:
        return False
    return nav

def process_weibo(element):
    msg = {}
    msg["mid"] = element.get_attribute("mid")
    msg["isforward"] = element.get_attribute("isforward")
    #msg["message"] = element.find_element_by_xpath("//p[@node-type='feed_list_content']").text
    msg["message"] = element.find_element_by_css_selector("p").text
    msg["pubdate"] = element.find_element_by_css_selector("p.info a.date").text
    ##pp(msg)
    return msg

def do_login(agent, timeout):
    debug('dologin')
    agent.get(SINA_LOGIN_URL)
    waiter = WebDriverWait(agent, timeout, 1)
    try:
        debug('dologin/waiter.util')
        waiter.until(lambda ag: check_login_succ(ag))
        debug('dologin/waiter.util/done')
    except NoSuchElementException:
        raise Exception("CodingError")
    except TimeoutException:
        raise Exception("LoginFail")

def do_fetch_weibo(agent, fname, url):
    debug('dofetch')
    agent.get(url) ## 打开页面
    fn = open("%s.json"%fname, "a+")
    debug('dofetch/get')
    ct = 0
    while True:
        debug('dofetch/get/fetchcycle%d'%ct)
        ct += 1

        waiter = WebDriverWait(agent, 600, 1)        ## wait the nav bar
        nav = waiter.until(lambda ag: check_nav_bar(ag))

        #contents = agent.find_elements_by_xpath("//dl[@action-type='feed_list_item']")
        contents = agent.find_elements_by_css_selector("div.feed_lists dl.feed_list")
        msgs = map(lambda el:process_weibo(el), contents)
        for msg in msgs:
            ##debug(msg['message'])
            #debug("dumptojson")
            fn.write(json.dumps(msg))
            fn.write("\n")
        try:
            btns = nav.find_elements_by_css_selector("a.W_btn_a")
            next_page = btns[1] if len(btns) == 2 else btns[0]
        except NoSuchElementException:
            traceback.print_exc()
            break
        if next_page.text != u'下一页':
            debug('next_page.text = %s'%next_page.text)
            break
        next_page.click()

def main():
    agent = init()
    targets = { 
                'aisk': 'http://weibo.com/aisk',
                'notedit': 'http://weibo.com/notedit',
                'gashero': 'http://weibo.com/u/1771197801',
                'soddyque': 'http://weibo.com/soddyque',
                'luc': 'http://weibo.com/luct',
                'zmm': 'http://weibo.com/zmmbreeze',
                'philip': 'http://weibo.com/philiptzou',
                'chang': 'http://weibo.com/jishubu',
                }
    targets = {
                'notedit': 'http://weibo.com/notedit',
                }
    try:
        do_login(agent, 600)
        for fname, url in targets.iteritems():
            do_fetch_weibo(agent, fname, url)
        ##time.sleep(1200)
    except:
        traceback.print_exc()
    finally:
        agent.close()

if '__main__' == __name__:
    main()
