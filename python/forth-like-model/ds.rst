===========================
vm design
===========================

:Author: jyf
:Date: 2012-04-09

.. contents:: index
.. sectnum::

Concepts
=====================

Name
---------

tweezer vm

Short Description
-----------------------

+ tiny and flexable

+ 32 bit as a cell

+ 64 bit as the bandwidth of bus

+ 2 stack, one for data, one for control

+ data stack contains ref-idx from the heap

+ data only has 4 type: interger, string, list, dict

+ control stack contains code address

+ there is some intrenal registers
    - ip register which indicate the next load address
    - port register which indicate the target port

commands
=====================

stack manipulates
------------------

DS
    data stack

CS
    control stack

+ push
    - push, 0x01, push data FROM DS[-1] to CS[-1]

+ pop
    - pop, 0x02, pop data from CS[-1] to DS[-1]

+ drop
    - dropds, 0x03, drop data from DS
    - dropcs, 0x04, drop data from CS

+ dup
    - dup, 0x05, duplicate data from DS

+ swap
    - swap, 0x06, swap data between DS[-1] and DS[-2]

+ rotate
    - rotate, 0x07, rotate data in DS, from DS[-3], DS[-2], DS[-1] to DS[-2], DS[-1], DS[-3]

+ load
    - load, 0x08, push data FROM the follow memory to CS[-1]

branchs
-----------------

all jump commands will pop address from CS[-1]

+ jump
    - jump, 0x09, jump directly to address in CS[-1]
    - beq, 0x0a, jump to address in CS[-1] if DS[-2] == DS[-1]
    - bez, 0x0b, jump to address in CS[-1] if DS[-1] == 0
    - blt, 0x0c, jump to address in CS[-1] if DS[-2] < DS[-1]
    - ble, 0x0d, jump to address in CS[-1] if DS[-2] <= DS[-1]
    - bgt, 0x0e, jump to address in CS[-1] if DS[-2] > DS[-1]
    - bge, 0x0f, jump to address in CS[-1] if DS[-2] >= DS[-1]
    - bneq, 0x10, jump to address in CS[-1] if DS[-2] != DS[-1]
    - bnez, 0x11, jump to address in CS[-1] if DS[-1] != 0

maths
-----------------

+ arithmetic
    - add, 0x12, drop DS[-2], DS[-1] and push (DS[-2]+DS[-1]) to DS
    - sub, 0x13, drop DS[-2], DS[-1] and push (DS[-2]-DS[-1]) to DS
    - mul, 0x14, drop DS[-2], DS[-1] and push (DS[-2]*DS[-1]) to DS[-2], DS[-1]
    - /mod, 0x15, drop DS[-2], DS[-1] and push (DS[-2]/DS[-1]) to DS[-2], (DS[-2]%DS[-1]) to DS[-1]
    - inc, 0x16, increase DS[-1]
    - dec, 0x17, increase DS[-1]

+ bit op
    - and, 0x18, drop DS[-2], DS[-1] and push (DS[-2] & DS[-1]) to DS
    - or, 0x19, drop DS[-2], DS[-1] and push (DS[-2] | DS[-1]) to DS
    - xor, 0x1a, drop DS[-2], DS[-1] and push (DS[-2] ^ DS[-1]) to DS
    - not, 0x1b, drop DS[-1] and push (!DS[-1]) to DS

+ shift
    - there is no shift commands, because we dont need it

services
-----------------

+ call, 0x1c, call service , the DS contains the params
    - DS[-1] is the services number
    - DS[-2] is the params length
    - params starts from DS[-3]

+ reserved service numbers, (0-255)
    - 0x00, vm stats query
    - 0x01, vm control

+ custermized service number
    - start from 0x0100
