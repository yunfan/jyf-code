## this is an fib test

start:
    load 36
    jump fib

fib:
    dup
    load 2
    bge fibelse
        dropds
        load 1
        jump print
    fibelse:
        load 1
        load 1

        rotate
        load 1
        add
        load 2
        push
        push

        loop:
            ## 2dup
            swap
            dup
            rotate
            dup
            rotate
            swap

            add
            rotate
            dropds

            pop
            pop
            load 1
            add

            ## 2dup
            swap
            dup
            rotate
            dup
            rotate
            swap

            ble fibend

            push
            push
            jump loop

fibend:
    dropds
    dropds

print:
    load 1
    load 257
    call
