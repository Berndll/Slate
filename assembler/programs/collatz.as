; Use port P0 as starting number
pld 0

; Check if even/odd
lir r1 1

.start
and r1
cpi 1
; If odd
brh eq .odd

# If even
ror
brh true .start

.odd
rst r2
rol
add r2
adi 1
brh true .start