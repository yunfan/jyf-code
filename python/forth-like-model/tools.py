#!/usr/bin/env python2.5
# -*- coding: utf-8 -*-

import sys
import time
import re
from struct import pack
from pprint import pprint as pp

OPLABEL = re.compile(r'''^([a-zA-Z:]+)''', re.U|re.I|re.M|re.S)
OP = re.compile(r'''^([a-zA-Z]+)''', re.U|re.I|re.M|re.S)
DIRECT = re.compile(r'''^.([a-zA-Z0-9]+)''', re.U|re.I|re.M|re.S)
INT = re.compile(r'''^([0-9a-fx.]+)''', re.U|re.I|re.M|re.S)
STR = re.compile(r'''^"([^"]+?)"''', re.U|re.I|re.M|re.S)

BRANCH = re.compile(r'''^(?P<op>[a-zA-Z]+)\s+(?P<label1>[a-zA-Z0-9]+)''', re.U|re.I|re.M|re.S)

OPCODES = {
    'push': 0x01,
    'pop': 0x02,
    'dropds': 0x03,
    'dropcs': 0x04,
    'dup': 0x05,
    'swap': 0x06,
    'rotate': 0x07,
    'load': 0x08,

    'jump': 0x09,
    'beq': 0x0a,
    'bez': 0x0b,
    'blt': 0x0c,
    'ble': 0x0d,
    'bgt': 0x0e,
    'bge': 0x0f,
    'bneq': 0x10,
    'bnez': 0x11,

    'add': 0x12,
    'sub': 0x13,
    'mul': 0x14,
    'mod': 0x15,
    'inc': 0x16,
    'dec': 0x17,
    'and': 0x18,
    'or': 0x19,
    'xor': 0x1a,
    'not': 0x1b,

    'call': 0x1c,

    }

def asm(inf, outf):
    ip = open(inf, "rb")

    header = [ord(c) for c in "this is a tweezer vm rom"]
    heap = []
    code = []

    ## check label
    loc = {}
    lno = 0
    offset = 0
    for l in ip.xreadlines():
        lno += 1
        l = l.strip()
        ##print lno, l
        if not l or l.startswith('#') or l.startswith('.'):
            ## blank line, only comment, direct
            continue
        else:
            m = OPLABEL.search(l)
            if not m:
                continue
            d = m.groups()[0]
            if d.endswith(':'):
                ## bind offset to label
                label = d[:-1].upper()
                if label in loc:
                    raise Exception("Label Name Duplicate: %s At Line %d" % (label, lno))
                ##print "found label [%s] at offset %d" % (label, offset)
                loc[label] = offset
            else:
                ## opcode
                op = d.lower()
                if op not in OPCODES:
                    raise Exception("Invalid Opcode: %s At Line %d" % (op, lno))

                if op in ('load', ):
                    offset += 2
                elif op in ('jump', 'bez', 'bnez', 'beq', 'blt', 'ble', 'bgt', 'bge', 'bneq'):
                    # load addr; push; op
                    offset += 4
                else:
                    offset += 1
                ##print "found opcode [%s] at offset %d" % (op, offset)

    ## compiling
    ip.seek(0)
    lno = 0
    for l in ip.xreadlines():
        lno += 1
        l = l.strip()
        if not l or l.startswith('#') or l.startswith('.'):
            ## blank line, only comment, direct
            continue
        else:
            m = OPLABEL.search(l)
            if not m:
                continue
            d = m.groups()[0]
            if d.endswith(':'):
                continue

            ## opcode
            op = d.lower()

            if op in ('load', ):
                ## the special load opcode
                code.append(OPCODES[op])
                l = l[4:].lstrip()
                m, n = INT.search(l), STR.search(l)
                if m:
                    d = m.groups()[0]
                    if d.startswith('0x'):
                        code.append(int(d, 16))
                    else:
                        code.append(int(d))
                elif n:
                    d = n.groups()[0]
                    heap_offset = len(heap)
                    for c in d:
                        # string should be encoded in utf-8
                        heap.append(ord(c))
                    heap.append(0)          ## zero-terminated
                    code.append(heap_offset)

            elif op in ('jump', 'bez', 'bnez', 'beq', 'blt', 'ble', 'bgt', 'bge', 'bneq'):
                m = BRANCH.search(l)
                if not m:
                    raise Exception("Invalid Syntax: %s At Line %d"%(op, lno))
                info = m.groupdict()
                label1 = info['label1'].upper()
                if label1 not in loc:
                    raise Exception("Reference for unknow label: %s At Line %d"% (label1, lno))
                code.append(OPCODES['load'])
                code.append(loc[label1])
                code.append(OPCODES['push'])
                code.append(OPCODES[op])

            else:
                code.append(OPCODES[op])

    code.append(0x00)
    ip.close()
    pp(heap)
    pp(code)
    ## build rom
    f = open(outf, 'wb')
    ## magic code
    f.write('TZVM')
    ## header size, heap size, code size
    f.write(pack('<3i', len(header)*4, len(heap)*4, len(code)*4))
    print len(heap)*4, len(code)*4
    ## header
    f.write(pack('<%di'%len(header), *header))
    ## heap
    f.write(pack('<%di'%len(heap), *heap))
    ## code
    f.write(pack('<%di'%len(code), *code))
    f.close()

def main():
    assert len(sys.argv) >= 3, "fuck off"
    inf, outf = sys.argv[1:3]
    assert inf.endswith('.s'), "input file need  to end with .s"
    assert outf.endswith('.rom'), "output file need to end with .rom"
    t1 = time.time()
    asm(inf, outf)
    t2 = time.time()
    print "build rom done! costs %f s" % (t2-t1)

if '__main__' == __name__:
    main()
