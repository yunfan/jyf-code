==========================================================
    design document
==========================================================

:File: ds.rst
:Date: 2010-04-22
:Author: jyf<jyf1987@gmail.com>

.. contents:: Index
.. sectnum::

OverView
=================================

a mini blog which can run at GAE platform


Target
=================================

#. run at GAE platform
#. single user
#. basic management of blogpost, tag, comment

Architecture
=================================

#. will dump to xml and json format, xml for browser, json for api and Ajaxual page
#. using webpy as the web framework
#. wont use GAE's user api, it's ugly
#. no html editor in manage layout, instead we support ubb code,like [img][/img]

Data Structure
=================================

BlogPost
----------------------------

================    ===================     ===================
key                     specs                   addional
title                   string                  require

tag                     array                   optional

================    ===================     ===================



Tag
----------------------------

Comment
----------------------------




