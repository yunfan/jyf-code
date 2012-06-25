#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: setting.py
# Date: 2009-11-25
# Author: jyf

import psycopg2

DB_PARAMS = {
    'creator': psycopg2,
    'host': 'localhost',
    'user': 'dbu',
    'database': 'reader'
}

FCGIPORT = 8601


##########################  sql ################################################
ITEM_ADD = """INSERT INTO shareitems (source,title,raw_url,short_url,add_user,from_ip) VALUES ( '%(source)s' , '%(title)s' , '%(raw_url)s' , '%(short_url)s' , '%(add_user)s' , '%(from_ip)s' )"""

