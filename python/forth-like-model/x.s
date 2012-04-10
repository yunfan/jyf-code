## this is an asm file for tweezer vm

init:
    load "hello, world"         ## $str_ref
    load 0x0f                   ## $loop_ctl

loop:
    load 1
    sub
    ## $loop_ctl -= 1
    swap
    dup
    ## [$loop_time, $str_ref, $str_ref]
    load 1      ## paragram length
    load 256      ## service number  256: customized service => print to stdout
    call    ## result depends on service . 1 has no result
    ## [$loop_time, $str_ref]
    swap
    dup
    ## [$str_ref, $loop_ctl, $loop_ctl]
    bnez loop

end:
