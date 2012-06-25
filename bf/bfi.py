#!/usr/bin/env python

import sys

stack = []
stack_max = 65536

class VmError(Exception):
    pass

def vm_init():
    global stack
    for i in range(stack_max):
        ##print i
        stack.append(0)

def vm_destroy():
    global stack
    
    i = 0
    while i < stack_max:
        if stack[stack_max - i] > 0:
            break
        else:
            i += 1
    
    i -= 1
    print "i = %d " % i

    #i = 65536 -16
    print "\nVm Dump"

    for j in range(0, stack_max-i, 16):
        print '0x%04X' % j , ' '*4, ' '.join(map(lambda c: '%02X' % c, stack[j:j+16]))


def vm_run(cmd, idx=0):
    global stack
    assert type(cmd) == str, 'cmd chunk should be a str type'

    vm_init()
    cmd_idx = 0
    cmd_len = len(cmd)
    curr_bit_offset = 0
    
    while cmd_idx < cmd_len:
        c = cmd[cmd_idx]
        ##print 'Debug: c = %s, idx = %d' % ( c, idx )
        if '>' == c:
            if idx+1 < stack_max:
                curr_bit_offset = 0
                idx += 1
            else:
                raise VmError("index out of range, max limitation")

        elif '<' == c:
            if idx > 0:
                curr_bit_offset = 0
                idx -= 1
            else:
                raise VmError("index out of range, min limitation")

        elif ';' == c:
            if curr_bit_offset < 8:
                curr_bit_offset += 1
            else:
                raise VmError("sorry, but we currently only support 8 bit")

        elif '\'' == c:
            if curr_bit_offset > 0:
                curr_bit_offset -= 1
            else:
                raise VmError("index should be positive number")

        elif '+' == c:
            if stack[idx] < 255:
                if curr_bit_offset == 0:
                    stack[idx] += 1
                else:
                    stack[idx] |= 2**curr_bit_offset
            else:
                #stack[idx] += 1
                #stack[idx] = 0
                pass

        elif '-' == c:
            if stack[idx] > 0:
                if curr_bit_offset == 0:
                    stack[idx] -= 1
                else:
                    stack[idx] &= (255 - 2**curr_bit_offset)
            else:
                #stack[idx] = 255
                pass

        elif '.' == c:
            sys.stdout.write(chr(stack[idx]))
            sys.stdout.flush()

        elif ',' == c:
            ## python's getkey sucks
            pass

        elif '[' == c:
            if stack[idx] == 0:
                oidx = idx
                p = 1
                while cmd_idx < cmd_len:
                    cmd_idx += 1
                    if cmd[cmd_idx] == '[':
                        p += 1
                    elif cmd[cmd_idx] == ']':
                        p -= 1
                    if p == 0 :
                        cmd_idx += 1
                        break 
                else:
                    raise VmError("couldnt find the matching pair ], from positon: %d" % oidx)


        elif ']' == c:
            if stack[idx] > 0:
                oidx = idx
                p = 1
                while cmd_idx > 0:
                    cmd_idx -= 1
                    ##print 'Debug: find matching [: cmd_idx = %d, cmd = %s, p = %d' % ( cmd_idx, cmd[cmd_idx], p )
                    if cmd[cmd_idx] == '[':
                        p -= 1
                    elif cmd[cmd_idx] == ']':
                        p += 1
                    if p == 0:
                        break
                else:
                    raise VmError("couldnt find the matching pair ], from positon: %d" % oidx)

        elif '!' == c:
            curr_bit_offset = 0
        else:
            pass
        
        ##print 'Debug: ',idx
        cmd_idx += 1

    print ''


def main():
    vm_init()
    cmd = """>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-]
    <.#>+++++++++++[<+++++>-]<.>++++++++[<+++>-]<.+++.------.--------.[-]>++++++++[
    <++++>-]<+.[-]++++++++++.>++++++++++++++++++++++++++++++++++++++++."""
    vm_run(cmd)
    vm_destroy()

def main_new():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    else:
        cmd = """+;;;;;;+."""
    vm_init()
    vm_run(cmd)
    #vm_destroy()


if '__main__' == __name__:
    main_new()
