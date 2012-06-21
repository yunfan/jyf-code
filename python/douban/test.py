# -*- coding: utf-8

from group import Group

##groups = ['beijingzufang', ]
groups = ['276176', '262626', '26926', '42745', 'sweethome']

for g_code in groups:
    g = Group(g_code)
    for info in g.fetch(0, 500):
        print info['title'].encode('utf-8'), info['link'], info['date']
