; Use port P0 as starting number
pld 0

; Check if even/odd
lir r1 1

.start
    ; Use port as output
    pst 0
    rst r7 ; Use R7 as temp
    and r1
    cpi 1
    ; If odd
    brh eq .odd

    ; If even
    rld r7
    rsh 0
    brh true .start

    ; Else
    .odd
        ; Calculate 3n
        rld r7
        rst r2
        lsh
        add r2
        ; Add 1
        adi 1
        ; Return to start
        brh true .start