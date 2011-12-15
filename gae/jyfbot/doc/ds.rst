=======================================================
    ds.rst
=======================================================

.. contents:: Index
.. sectnum::

Overview
==================

RPC style server
Support Multiple Channel(mail, gtalk, http? these are all fetures :D )
Automatic notify will be supported by out app(like use an out app to request the notify uri when time)

Rpc and Envir
==================

#. we use cmd router mode like::
    
    (
        (r'regex', func),
        (r'regex', func),
        (r'.*', func)       ## This is the "Not Found" process
    )

#. each request will generate a req object,it will has the structure like::

    {
        "from": {"full": "jyf1987@gmail.com/office", "node": "jyf1987", "domain": "gmail.com", "resource": "office"},
        "argv": ["\1", "\2", ... ],
        "raw": "raw msg"
    }

#. each call will return a text/html contents, it will be return to the request user

License
=================

check the COPYING, i am serious, i choose the WTFPL , you must use the code under that, :D

May 42 bless you
