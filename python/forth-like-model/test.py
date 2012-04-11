#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import vm

def srv_print(env, str_ref):
    heap = env['heap']
    tstr = []
    c = heap[str_ref]
    while c != 0:
        tstr.append(chr(c))
        str_ref += 1
        c = heap[str_ref]
    tstr = ''.join(tstr)
    print tstr

def srv_print_int(env, int_val):
    print int_val

def main():
    assert len(sys.argv) >= 2, "fuck off"
    romfile = sys.argv[1]
    assert romfile.endswith('.rom'), "rom file need to end with .rom"

    rp = open(romfile, 'rb')
    tvm = vm.TweezerVm(rp)
    tvm.register_service(256, srv_print)
    tvm.register_service(257, srv_print_int)
    tvm.run()
    ##env = tvm._env
    ##print env['code'][env['ip']]

if '__main__' == __name__:
    main()
