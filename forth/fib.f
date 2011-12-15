: fib ( n -- m ) dup 2 <
    if
        drop 1
    else
        1 1 rot 1+ 2
        do
            2dup + rot drop
        loop
    then ;

36 fib . cr bye
