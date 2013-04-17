#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class BFVM(object):
    def __init__(self, code):
        self.CODE = code
        self.CL = len(self.CODE)    ## Code Length
        self.SP = 0

        self.DATA = [0]
        self.DP = 0         ## Data Pointer
        self.DL = 1         ## Data Length

        self.CS = []
        self.ST = 'EXEC'

    def run_step(self, step):
        idx = 0
        while idx != step:
            code = self.CODE[self.SP]
            st = self.ST

            if st == 'EXEC':

                if code == '<':
                    self.DP -= 1        ## well in python, a positive number index like self.DATA[-1] wont raise error

                elif code == '>':
                    self.DP += 1
                    if self.DL <= self.DP:
                        self.DL = self.DP + 1
                        self.DATA.append(0)

                elif code == '+':
                    self.DATA[self.DP] += 1

                elif code == '-':
                    self.DATA[self.DP] -= 1      ## maybe we should prevent positive number? but who care if you dont print it?

                elif code == '[':
                    if self.DATA[self.DP] == 0:
                        self.ST = 'SKIP'
                    else:
                        self.CS.append(self.SP)

                elif code == ']':
                    if self.DATA[self.DP] != 0:
                        self.SP = self.CS[-1]
                    else:
                        self.CS.pop()   ## might raise error if you wrote wrong code

                elif code == ',':
                    s = raw_input()
                    self.DATA[self.DP] = ord(s[0])

                elif code == '.':
                    sys.stdout.write(chr(self.DATA[self.DP]))
                    ##print chr(self.DATA[self.DP]), '%d' % self.DATA[self.DP]

            elif st == 'SKIP':
                if code == ']':
                    self.ST = 'EXEC'

            idx += 1
            self.SP += 1
            if self.SP >= self.CL:
                break       ## here we have arrive the end of code

    def run(self):
        self.run_step(-1)

def main():
    cmd = """>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-]
    <.#>+++++++++++[<+++++>-]<.>++++++++[<+++>-]<.+++.------.--------.[-]>++++++++[
    <++++>-]<+.[-]++++++++++.>++++++++++++++++++++++++++++++++++++++++."""
    ##cmd = """>+++++[<+++++>-]<."""
    vm = BFVM(cmd)
    vm.run()

    """
    for idx in xrange(30):
        print "idx: %d" % idx
        print "CL = %d, SP = %d" % (vm.CL, vm.SP)
        print "DATA = %s, DP = %d, DL = %d" % (repr(vm.DATA), vm.DP, vm.DL)
        print "CS = %s, ST = %s" % (repr(vm.CS), vm.ST)
        print ""
        vm.run_step(1)
    """

def main_new():
    if len(sys.argv) > 1:
        fn = sys.argv[1]
        cmd = open(fn, 'r').read()
    else:
        cmd = """>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-]
        <.#>+++++++++++[<+++++>-]<.>++++++++[<+++>-]<.+++.------.--------.[-]>++++++++[
        <++++>-]<+.[-]++++++++++.>++++++++++++++++++++++++++++++++++++++++."""

    vm = BFVM(cmd)
    vm.run()

    """
    for idx in xrange(500):
        print "idx: %d" % idx
        print "CL = %d, SP = %d" % (vm.CL, vm.SP)
        print "DATA = %s, DP = %d, DL = %d" % (repr(vm.DATA), vm.DP, vm.DL)
        print "CS = %s, ST = %s" % (repr(vm.CS), vm.ST)
        print "CODE = %s" % (vm.CODE[vm.SP])
        print ""
        vm.run_step(1)
    """


if '__main__' == __name__:
    main_new()
