#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
from struct import unpack
from pprint import pprint as pp

def _stack_cmd(cmd, env):
    if cmd == 0x01:
        ## push
        env['cs'].append(env['ds'].pop())
    elif cmd == 0x02:
        ## pop
        env['ds'].append(env['cs'].pop())
    elif cmd == 0x03:
        ## dropds
        env['ds'].pop()
    elif cmd == 0x04:
        ## dropcs
        env['cs'].pop()
    elif cmd == 0x05:
        ## dup
        env['ds'].append(env['ds'][-1])
    elif cmd == 0x06:
        # swap
        fst, sec = env['ds'].pop(), env['ds'].pop()
        env['ds'].append(fst)
        env['ds'].append(sec)
    elif cmd == 0x07:
        # rotate
        fst, sec, thd = env['ds'].pop(), env['ds'].pop(), env['ds'].pop()
        env['ds'].append(sec)
        env['ds'].append(fst)
        env['ds'].append(thd)
    elif cmd == 0x08:
        ## load
        env['ip'] += 1
        env['ds'].append(env['code'][env['ip']])
    ##print env['ds'], env['cs']
    env['ip'] += 1

def _branch_cmd(cmd, env):
    addr = env['cs'].pop()
    if cmd == 0x09:
        ## jump
        env['ip'] = addr
    elif cmd == 0x0a:
        ## beq
        fst, sec = env['ds'].pop(), env['ds'].pop()
        env['ip'] = addr if sec == fst else env['ip'] + 1
    elif cmd == 0x0b:
        ## bez
        fst = env['ds'].pop()
        env['ip'] = addr if fst == 0 else env['ip'] + 1
    elif cmd == 0x0c:
        ## blt
        fst, sec = env['ds'].pop(), env['ds'].pop()
        env['ip'] = addr if sec < fst else env['ip'] + 1
    elif cmd == 0x0d:
        ## ble
        fst, sec = env['ds'].pop(), env['ds'].pop()
        env['ip'] = addr if sec <= fst else env['ip'] + 1
    elif cmd == 0x0e:
        ## bgt
        fst, sec = env['ds'].pop(), env['ds'].pop()
        env['ip'] = addr if sec > fst else env['ip'] + 1
    elif cmd == 0x0f:
        ## bge
        fst, sec = env['ds'].pop(), env['ds'].pop()
        env['ip'] = addr if sec >= fst else env['ip'] + 1
    elif cmd == 0x10:
        ## bneq
        fst, sec = env['ds'].pop(), env['ds'].pop()
        env['ip'] = addr if sec != fst else env['ip'] + 1
    elif cmd == 0x11:
        ## bnez
        fst = env['ds'].pop()
        env['ip'] = addr if fst != 0 else env['ip'] + 1
    ##print env['ds'], env['cs']

def _math_cmd(cmd, env):
    if cmd == 0x12:
        ## add
        fst, sec = env['ds'].pop(), env['ds'].pop()
        env['ds'].append(sec + fst)
    elif cmd == 0x13:
        ## sub
        fst, sec = env['ds'].pop(), env['ds'].pop()
        env['ds'].append(sec - fst)
    elif cmd == 0x14:
        ## mul
        fst, sec = env['ds'].pop(), env['ds'].pop()
        res = fst*sec
        env['ds'].append(res/2**32)
        env['ds'].append(res%2**32)
    elif cmd == 0x15:
        ## /mod
        fst, sec = env['ds'].pop(), env['ds'].pop()
        env['ds'].append(sec/fst)
        env['ds'].append(sec%fst)
    elif cmd == 0x16:
        ## inc
        env['ds'][-1] += 1
    elif cmd == 0x17:
        ## dec
        env['ds'][-1] -= 1
    elif cmd == 0x18:
        ## and
        fst, sec = env['ds'].pop(), env['ds'].pop()
        env['ds'].append(sec & fst)
    elif cmd == 0x19:
        ## or
        fst, sec = env['ds'].pop(), env['ds'].pop()
        env['ds'].append(sec | fst)
    elif cmd == 0x1a:
        ## xor
        fst, sec = env['ds'].pop(), env['ds'].pop()
        env['ds'].append(sec ^ fst)
    elif cmd == 0x1b:
        ## not
        fst = env['ds'].pop()
        env['ds'].append(~fst)
    ##print env['ds'], env['cs']
    env['ip'] += 1

def _service_cmd(cmd, env):
    if cmd != 0x1c:
        env['ip'] += 1
        return
    num, plen = env['ds'].pop(), env['ds'].pop()
    ##print plen, num
    ##pp(env['ds'])
    args = [env['ds'].pop() for idx in xrange(plen)]
    svr_pool = 'sys_services' if num < 256 else 'custom_services'
    srv = env[svr_pool].get(num, None)
    if callable(srv):
        srv(env, *args)
    ##print env['ds'], env['cs']
    env['ip'] += 1

class TweezerVm(object):
    def __init__(self, romfile):
        self.reset()
        self.load_rom(romfile)
        ## binding _stack_cmd
        [self.slot.__setitem__(srv_num, _stack_cmd) for srv_num in xrange(0x09)]
        ## binding _stack_cmd
        [self.slot.__setitem__(srv_num, _branch_cmd) for srv_num in xrange(0x09, 0x12)]
        ## binding _math_cmd
        [self.slot.__setitem__(srv_num, _math_cmd) for srv_num in xrange(0x12, 0x1c)]
        ## binding _service_cmd
        self.slot[0x1c] = _service_cmd

    def load_rom(self, romfile):
        MAGIC = romfile.read(4)
        if MAGIC != 'TZVM':
            raise Exception('this is not a valid rom file: MAGIC invalid')
        header_size, heap_size, code_size = unpack('<3i', romfile.read(12))
        ##print >>sys.stderr, 'header_size: %d, heap_size: %d, code_size: %d' % (header_size, heap_size, code_size)
        if heap_size % 4 != 0 or code_size % 4 != 0:
            raise Exception('this is not a valid rom file: HEAP_SIZE or CODE_SIZE unalign')
        ## i dont care header
        heap_len = heap_size/4
        code_len = code_size/4

        romfile.seek(romfile.tell() + header_size)
        self._env['heap'] = list(unpack('<%di'%heap_len, romfile.read(heap_size)))
        ##pp(self._env['heap'])

        codes = romfile.read(code_size)
        ##pp(unpack('<%di'%(len(codes)/4), codes))
        self._env['code'] = list(unpack('<%di'%code_len, codes))

    def run(self, addr=0):
        env = self._env
        env['ip'] = addr
        while True:
            cmd = self._env['code'][env['ip']]
            if cmd == 0x00:
                return
            try:
                self.slot[cmd](cmd, env)
            except:
                traceback.print_exc()
                ##pp(self._env)
                return

    def reset(self):
        self._env = {
            'ip': 0,
            'ds': [],
            'cs': [],
            'heap': [],
            'code': [],
            'sys_services': {},
            'custom_services': {},
            }
        self.slot = {}
        return

    def register_service(self, serv_num, callb):
        if serv_num < 256:
            return False
        self._env['custom_services'][serv_num] = callb
        return True

    def dump(self):
        pp(self._env)

