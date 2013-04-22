#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools

def chunk_split_test():

    chunk_split = lambda s, N, d: d.join(''.join(row) for row in (i for i in itertools.izip_longest(*itertools.repeat(iter(s), N), fillvalue='')))

    a = 'abcdefghijk'.upper()

    print chunk_split(a, 2, ':')
    print chunk_split(a, 3, ':')

def fold_Nth_test():

    fold_nth = lambda iterable, N: itertools.izip_longest(*itertools.repeat(iter(iterable), N), fillvalue=None)     ## the default fillvalue is None, but i want to claim it again in code

    m = range(9)

    print list(fold_nth(m, 2))
    print [filter(lambda e: e is not None, r) for r in fold_nth(m, 2)]


def test():
    chunk_split_test()
    fold_Nth_test()

test()
