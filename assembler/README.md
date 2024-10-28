# TO NOTE
Instructions which need two cycles - notably BRH and CAL - would have to be followed by a NOP with the upper address as an operand.
The assembler adds an extra instruction for this, called "UPA" (Upper Address) which should be used instead.