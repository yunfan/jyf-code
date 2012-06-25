================================
Virtual CPU Design
================================

:Author: jyf
:Date: 2012-02-16

.. contents:: Index
.. sectnum::

concept
================

endian
    little endian

word
    32bit

register
    32 general purpose 32bit register
    and it has dual register file for quickly switching

ram
    1024 KB size
    real mode
    load/store anywhere

opcodes
    + RISC model
    + each opcode costs a word
    + different opcodes cost different cycles from 1 - 100

opcodes details
=======================

all opcodes costs a word size.

and the first 6bit is used for opcode identify, the left 24bit for params

we will use a c struct to represent that

math operations
------------------

add
~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b000001
        unsigned dst:5;         // register id , register to store the value(r0-r31)
        unsigned src1:5;        // register id , register to add from
        unsigned src2:5;        // register id , register to add to
    } op_add;

$dst = $src1 + $src2

it cost 1 cycle

sub
~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b000010
        unsigned dst:5;         // register id , register to store the value
        unsigned src1:5;        // register id , register to subtract from
        unsigned src2:5;        // register id , register to subtract
    } op_sub;


$dst = $src1 - $src2

it cost 1 cycle

multiply
~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b000011
        unsigned dst_hi:5;      // register id , register to store the high value
        unsigned dst_lo:5;      // register id , register to store the low value
        unsigned src1:5;        // register id , register to multiply from
        unsigned src2:6;        // register id , register to multiply
    } op_mul;


($dst_hi,$dst_lo) = $src1 * $src2

it cost 16 cycle

divide
~~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b000100
        unsigned dst_q:5;       // register id , register to store the quotient
        unsigned dst_r:5;       // register id , register to store the remainder
        unsigned src1:5;        // register id , register to divide from
        unsigned src2:5;        // register id , register to divide
    } op_div;

$dst_r = $src1 / $src2
$dst_q = $src1 % %src2

it cost 32 cycle

bit operations
-------------------

shift left
~~~~~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b000101
        unsigned dst:5;         // register id , register to store the result
        unsigned src:5;         // register id , register to get the origin value
        unsigned offset:5;      // small int, shift offset
    } op_sl;

$dst = $src << offset

it cost 1 cycle

shift right
~~~~~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b000110
        unsigned dst:5;         // register id , register to store the result
        unsigned src:5;         // register id , register to get the origin value
        unsigned offset:5;      // small int, shift offset
    } op_sr;

$dst = $src >> offset

it cost 1 cycle

bit and
~~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b000111
        unsigned dst:5;         // register id , register to store the result
        unsigned src1:5;        // register id , register to and from
        unsigned src2:5;        // register id , register to and from
    } op_and;

$dst = $src1 & $src2

it cost 1 cycle

bit or
~~~~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b001000
        unsigned dst:5;         // register id , register to store the result
        unsigned src1:5;        // register id , register to or from
        unsigned src2:5;        // register id , register to or from
    } op_or;

$dst = $src1 | $src2

it cost 1 cycle

bit xor
~~~~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b001001
        unsigned dst:5;         // register id , register to store the result
        unsigned src1:5;        // register id , register to nor from
        unsigned src2:5;        // register id , register to nor from
    } op_xor;

$dst = $src1 ^ $src2

it cost 1 cycle

bit not
~~~~~~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b001010
        unsigned dst:5;         // register id , register to store the result
        unsigned src:5;        // register id , register to not from
    } op_not;

$dst = ~($src)

it cost 1 cycle

jump and branch operations
-------------------------------

jump
~~~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b001011
        unsigned addr:18;       // int , the addr for jumping to which is a word addr means the real addr = this_addr * 4
    } op_jmp;

jump to (addr * 4)

it cost 1 cycle

branch when equal
~~~~~~~~~~~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b001100
        unsigned dst1:5;        // register id , the register store the destine addr
        unsigned dst2:5;        // register id , the register store the destine addr
        unsigned src1:5;        // register id , the register store the compare value
        unsigned src2:5;        // register id , the register store the compare value
    } op_be;

if $src1 == $src2:
    jmp ($dst1 * 4)
else:
    jmp ($dst2 * 4)

it cost 4 cycle

branch when greater
~~~~~~~~~~~~~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b001101
        unsigned dst1:5;        // register id , the register store the destine addr
        unsigned dst2:5;        // register id , the register store the destine addr
        unsigned src1:5;        // register id , the register store the compare value
        unsigned src2:5;        // register id , the register store the compare value
    } op_bgt;

if $src1 > $src2:
    jmp ($dst1 * 4)
else:
    jmp ($dst2 * 4)

it cost 4 cycle

branch when greater or equal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b001110
        unsigned dst1:5;        // register id , the register store the destine addr
        unsigned dst2:5;        // register id , the register store the destine addr
        unsigned src1:5;        // register id , the register store the compare value
        unsigned src2:5;        // register id , the register store the compare value
    } op_bge;

if $src1 >= $src2:
    jmp ($dst1 * 4)
else:
    jmp ($dst2 * 4)

it cost 4 cycle

data transfer operations
------------------------------

copy between registers
~~~~~~~~~~~~~~~~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b001111
        unsigned dst:5;         // register id , the register to copy to
        unsigned src:5;         // register id , the register to copy from
    } op_cpy;

$dst = $src

it cost 1 cycle

load from memory
~~~~~~~~~~~~~~~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b010000
        unsigned dst:5;         // register id , the register store the value
        unsigned addr:5;        // register id , the register which contain the addr
    } op_ldr;

$dst = load ($addr * 4)

it cost 4 cycle

store to memory
~~~~~~~~~~~~~~~~~~~~~~~
::

    typedef struct {
        unsigned id:6;          // id = 0b010001
        unsigned addr:5;        // register id , the register which contain the destine addr
        unsigned src:5;         // register id , the register store the value
    } op_ldr;

($addr * 4) <= $src

it cost 4 cycle
