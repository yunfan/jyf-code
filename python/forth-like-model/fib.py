#!/usr/bin/env python
# -*- coding: utf-8 -*-

def fib(n):
    if n <= 2:
        return 1
    else:
        a, b = 1, 1
        for idx in xrange(2, n+1):
            a, b = b, a+b
        return b

print fib(36)
