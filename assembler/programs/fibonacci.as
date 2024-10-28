.setup
lir r1 0
lir r2 1
lia 0

.loop
add r1
rst r1
add r2
rst r2
brh true .loop